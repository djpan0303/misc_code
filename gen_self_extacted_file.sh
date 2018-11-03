#!/bin/bash
function usage()
{
	echo "这个脚本用来创建自解压的安装包"
	echo "安装包目录结构应该如下："
	echo "--------PackageFile"
	echo -e "\t--install.sh"
	echo -e "\t--app1"
	echo -e "\t--app2"
	echo "app1为应用1，app2为应用2。install.sh负责对app1和app2进行安装。用户需要自己编写install.sh"
	echo "用法：$0 pkg_name out_file_name"
	echo "生成的安装包跟脚本在同一个位置"
}

function promt_and_abort() 
{
	echo $1
	exit 1
}

function abort_if_last_cmd_fail()
{	
	if [ $? -ne 0 ];then
		promt_and_abort $1
	fi
}

InstalledPackage=$1
if [ "x" = "x${InstalledPackage}" ];then
	usage
	promt_and_abort "ERROR:请指定要压缩的安装包pkg_name"
fi

if [ ! -d ${InstalledPackage} ];then
	usage
	promt_and_abort "ERROR:${InstalledPackage} 不是一个目录"
fi

OutputFile=$2
if [ "x" = "${OutputFile}x" ];then
	usage
	promt_and_abort "ERROR:请制定输出文件out_file_name的名字"
fi

InstalledPackage=${InstalledPackage%/*}
TarFile="${InstalledPackage}.bz"

tar jcvf ${TarFile} ${InstalledPackage}
abort_if_last_cmd_fail "create bz file fail"

#gen header
TMP_HEADER=".installer_header"
cat << 'END_TEXT' > ${TMP_HEADER}
#!/bin/bash
#test ${UID} -ne 0 && echo "WARNING:this package needs to be run as root!!!" && exit 1; 
echo -e "\nSelf Extracting...\n"

TMPDIR=/tmp
ARCHIVE=`awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0`
test -d $TMPDIR/asset && rm -rf $TMPDIR/asset;
tail -n+$ARCHIVE $0 | tar xj -C $TMPDIR
( cd $TMPDIR/asset; ./install.sh; cd ..;  rm -rf asset )

#reboot
# never remove the line below
exit 0
__ARCHIVE_BELOW__
END_TEXT

cat ${TMP_HEADER} ${TarFile} >> ${OutputFile}; chmod 755 ${OutputFile};
rm -f ${TarFile};
rm -f ${TMP_HEADER}
