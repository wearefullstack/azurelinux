# Name of the package without any prefixes
%global majorname mysql
%global package_version 8.4.3
%define majorversion %(echo %{package_version} | cut -d'.' -f1-2 )
%global pkgnamepatch mysql

# Set if this package will be the default one in distribution
%{!?mysql_default:%global mysql_default 1}

# AZL: we run as a root and the tests fail if ran as root, skipping them
# Regression tests may take a long time (many cores recommended), skip them by
# passing --nocheck to rpmbuild or by setting runselftest to 0 if defining
# --nocheck is not possible (e.g. in koji build)
%{!?runselftest:%global runselftest 0}

# Set this to 1 to see which tests fail, but 0 on production ready build
%global ignore_testsuite_result 0

# The last version on which the full testsuite has been run
# In case of further rebuilds of that version, don't require full testsuite to be run
# run only "main" suite
%global last_tested_version 8.0.40
# Set to 1 to force run the testsuite even if it was already tested in current version
%global force_run_testsuite 0

# Filtering: https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
%global __requires_exclude ^perl\\((hostnames|lib::mtr|lib::v1|mtr_|My::))
%global __provides_exclude_from ^(%{_datadir}/(mysql|mysql-test)/.*|%{_libdir}/mysql/plugin/.*\\.so)$

%global skiplist platform-specific-tests.list

%global boost_bundled_version 1.77.0

# When there is already another package that ships /etc/my.cnf,
# rather include it than ship the file again, since conflicts between
# those files may create issues

# For deep debugging we need to build binaries with extra debug info
%define debug 0

# Aditional SELinux rules from a standalone package 'mysql-selinux' (that holds rules shared between MariaDB and MySQL)
%define require_mysql_selinux 1


# Include files for systemd
%global daemon_name       mysqld
%global daemon_no_prefix  mysqld

# We define some system's well known locations here so we can use them easily
# later when building to another location (like SCL)
%global logrotateddir     %{_sysconfdir}/logrotate.d
%global logfiledir        %{_localstatedir}/log/mysql
%global logfile           %{logfiledir}/%{daemon_no_prefix}.log
# Directory for storing pid file
%global pidfiledir        %{_rundir}/%{daemon_name}
# Defining where database data live
%global dbdatadir         %{_localstatedir}/lib/mysql


# Set explicit conflicts with 'mariadb' packages
%define conflicts_mariadb 1
# Provide explicitly the 'community-mysql' names
#   'community-mysql' names are deprecated and to be removed in future Fedora
#   but we're leaving them here for compatibility reasons
%define provides_community_mysql %{?mysql_default}
# Obsolete the package 'community-mysql' and all its sub-packages
%define obsoletes_community_mysql %{?mysql_default}
# This is the last version of the 'community-mysql' package production release
%global obsolete_community_mysql_version 8.0.35-10
%global community_mysql_version 8.0.36-1

Summary:        MySQL.
Name:           mysql
Version:        8.4.3
Release:        1%{?dist}
License:        GPLv2 with exceptions AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Databases
URL:            https://www.mysql.com
Source0:        https://dev.mysql.com/get/Downloads/MySQL-8.0/%{name}-%{version}.tar.gz
# https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.4.3.tar.gz
Source2:          mysql_config_multilib.sh
Source3:          my.cnf
Source6:          README.mysql-docs
Source7:          README.mysql-license
Source10:         mysql.tmpfiles.d
Source11:         mysql.service
Source12:         mysql-prepare-db-dir.sh
Source14:         mysql-check-socket.sh
Source15:         mysql-scripts-common.sh
Source17:         mysql-wait-stop.sh
Source18:         mysql@.service
# To track rpmlint warnings
Source30:         %{pkgnamepatch}.rpmlintrc
# Configuration for server
Source31:         server.cnf
# Skipped tests lists
Source50:         rh-skipped-tests-list-base.list
Source51:         rh-skipped-tests-list-arm.list
Source52:         rh-skipped-tests-list-s390.list
Source53:         rh-skipped-tests-list-ppc.list

BuildRequires:    abseil-cpp
BuildRequires:    abseil-cpp-devel
BuildRequires:    cmake
BuildRequires:    gcc-c++
BuildRequires:    libaio-devel
BuildRequires:    libedit-devel
BuildRequires:    libevent-devel
BuildRequires:    libicu-devel
BuildRequires:    lz4-devel
BuildRequires:    bison
BuildRequires:    libzstd-devel
BuildRequires:    libcurl-devel
%ifnarch aarch64 s390x
BuildRequires:    numactl-devel
%endif
BuildRequires:    openssl
BuildRequires:    openssl-devel
%if 0%{?fedora} >= 41
# Complement of mysql-openssl-engine.patch
BuildRequires:    openssl-devel-engine
%endif

BuildRequires:    python3-devel
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
BuildRequires:    rpcgen
BuildRequires:    libtirpc-devel
BuildRequires:    protobuf-devel
BuildRequires:    zlib-devel
# Tests requires time and ps and some perl modules
BuildRequires:    procps
BuildRequires:    time
BuildRequires:    perl(base)
BuildRequires:    perl(Carp)
BuildRequires:    perl(Cwd)
BuildRequires:    perl(Digest::file)
BuildRequires:    perl(Digest::MD5)
BuildRequires:    perl(English)
BuildRequires:    perl(Env)
BuildRequires:    perl(Errno)
BuildRequires:    perl(Exporter)
BuildRequires:    perl(Fcntl)
BuildRequires:    perl(File::Copy)
BuildRequires:    perl(File::Find)
BuildRequires:    perl(File::Spec)
BuildRequires:    perl(File::Spec::Functions)
BuildRequires:    perl(File::Temp)
BuildRequires:    perl(FindBin)
BuildRequires:    perl(Data::Dumper)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(if)
BuildRequires:    perl(IO::File)
BuildRequires:    perl(IO::Handle)
BuildRequires:    perl(IO::Select)
BuildRequires:    perl(IO::Socket::INET)
BuildRequires:    perl(IPC::Open3)
BuildRequires:    perl(JSON)
BuildRequires:    perl(lib)
BuildRequires:    perl(LWP::Simple)
BuildRequires:    perl(Memoize)
BuildRequires:    perl(Net::Ping)
BuildRequires:    perl(POSIX)
BuildRequires:    perl(Socket)
BuildRequires:    perl(strict)
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Test::More)
BuildRequires:    perl(Time::HiRes)
BuildRequires:    perl(Time::localtime)
BuildRequires:    perl(warnings)
BuildRequires:    systemd

# Since MySQL 8.0.28
%{?with_fido:BuildRequires:    libfido2-devel}

%{?with_kerberos:BuildRequires:    krb5-devel}
%{?with_ldap:BuildRequires:    openldap-devel cyrus-sasl-devel cyrus-sasl-scram}

Requires:         bash coreutils grep

# 'boost' header files must be bundled
# See https://bugzilla.redhat.com/show_bug.cgi?id=2260138#c7 for details
Provides:         bundled(boost) = %{boost_bundled_version}

# 'rapidjson' library must be bundled
# The rapidjson upstream made the last release in 2016, even though it has an active development till today (2024, ~750 commits since)
# The MySQL upstream forked the project from a specific commit and added custom patches. See "extra/RAPIDJSON-README" for details.
# In the MySQL 8.0.34, the MySQL upsstream made the 'rapidjson' library to be bundled by default.
Provides:         bundled(rapidjson)

# Not available in Fedora
# https://github.com/martinus/unordered_dense
Provides:         bundled(unordered_dense)

%{?with_conflicts_mariadb:Conflicts: mariadb}
# Explicitly disallow installation of mysql + mariadb-server
%{?with_conflicts_mariadb:Conflicts: mariadb-server}
%{?with_provides_community_mysql:Provides: community-mysql = %community_mysql_version}
%{?with_provides_community_mysql:Provides: community-mysql%{?_isa} = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql <= %obsolete_community_mysql_version}

%define conflict_with_other_streams() %{expand:\
Provides: %{majorname}%{?1:-%{1}}-any\
Conflicts: %{majorname}%{?1:-%{1}}-any\
}

# Provide also mysqlX.X if default
%if %?mysql_default
%define mysqlX_if_default() %{expand:\
Provides: mysql%{majorversion}%{?1:-%{1}}\
Provides: mysql%{majorversion}%{?1:-%{1}}%{?_isa}\
}
%else
%define mysqlX_if_default() %{nil}
%endif

%define add_metadata() %{expand:\
%conflict_with_other_streams %{**}\
%mysqlX_if_default %{**}\
}

%add_metadata

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MySQL client programs and generic MySQL files.

%package          config
Summary:          The config files required by server and client
%{?with_provides_community_mysql:Provides: community-mysql-config = %community_mysql_version}
%{?with_provides_community_mysql:Provides: community-mysql-config%{?_isa} = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql-config <= %obsolete_community_mysql_version}

%add_metadata config

%description      config
The package provides the config file my.cnf and my.cnf.d directory used by any
MariaDB or MySQL program. You will need to install this package to use any
other MariaDB or MySQL package if the config files are not provided in the
package itself.


%package          common
Summary:          The shared files required for MySQL server and client
BuildArch:        noarch
%if 0%{?flatpak}
Requires:         mariadb-connector-c-config
%else
Requires:         %{_sysconfdir}/my.cnf
%endif
%{?with_provides_community_mysql:Provides: community-mysql-common = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql-common <= %obsolete_community_mysql_version}

# As this package is noarch, it can't use the %%{?_isa} RPM macro
%conflict_with_other_streams common

%description      common
The mysql-common package provides the essential shared files for any
MySQL program. You will need to install this package to use any other
MySQL package.


%package          libs
Summary:          The shared libraries required for MySQL clients
Requires:         mysql-common

%add_metadata libs

%description      libs
The mysql-libs package provides the essential shared libraries for any
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.


%package          errmsg
Summary:          The error messages files required by MySQL server
BuildArch:        noarch
Requires:         mysql-common
%{?with_provides_community_mysql:Provides: community-mysql-errmsg = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql-errmsg <= %obsolete_community_mysql_version}

# As this package is noarch, it can't use the %%{?_isa} RPM macro
%conflict_with_other_streams errmsg

%description      errmsg
The package provides error messages files for the MySQL daemon



%package          server
Summary:          The MySQL server and related files

Requires:         mysql

Requires:         mysql-common
%if 0%{?flatpak}
Requires:         mariadb-connector-c-config
%else
Requires:         %{_sysconfdir}/my.cnf
Requires:         %{_sysconfdir}/my.cnf.d
%endif
Requires:         mysql-errmsg
Requires:         coreutils
Requires(pre):    /usr/sbin/useradd
# We require this to be present for %%{_tmpfilesdir}
Requires:         systemd
# Make sure it's there when scriptlets run, too
%{?systemd_requires: %systemd_requires}
# SYS_NICE capabilities; #1540946
Recommends:       libcap
# semanage
Requires(post):   policycoreutils-python-utils

# Aditional SELinux rules (common for MariaDB & MySQL) shipped in a separate package
# For cases, where we want to fix a SELinux issues in MySQL sooner than patched selinux-policy-targeted package is released
%if %{with require_mysql_selinux}
Requires:         (mysql-selinux if selinux-policy-targeted)
%endif

%{?with_conflicts_mariadb:Conflicts: mariadb-server}
%{?with_conflicts_mariadb:Conflicts: mariadb-server-utils}
%{?with_conflicts_mariadb:Conflicts: mariadb-server-galera}
# Explicitly disallow installation of mysql + mariadb-server
%{?with_conflicts_mariadb:Conflicts: mariadb}
%{?with_provides_community_mysql:Provides: community-mysql-server = %community_mysql_version}
%{?with_provides_community_mysql:Provides: community-mysql-server%{?_isa} = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql-server <= %obsolete_community_mysql_version}

%add_metadata server

%description      server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.


%package          devel
Summary:          Files for development of MySQL applications
Requires:         openssl-devel
Requires:         zlib-devel
Requires:         libzstd-devel
%{?with_conflicts_mariadb:Conflicts: mariadb-devel}
%{?with_conflicts_mariadb:Conflicts: mariadb-connector-c-devel}
%{?with_provides_community_mysql:Provides: community-mysql-devel = %community_mysql_version}
%{?with_provides_community_mysql:Provides: community-mysql-devel%{?_isa} = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql-devel <= %obsolete_community_mysql_version}

%add_metadata devel

%description      devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.


%if %{with test}
%package          test
Summary:          The test suite distributed with MySQL
Requires:         mysql
Requires:         mysql-common
Requires:         mysql-server%{?_isa}
Requires:         gzip
Requires:         lz4
Requires:         openssl
Requires:         perl(Digest::file)
Requires:         perl(Digest::MD5)
Requires:         perl(Env)
Requires:         perl(Exporter)
Requires:         perl(Fcntl)
Requires:         perl(File::Temp)
Requires:         perl(FindBin)
Requires:         perl(Data::Dumper)
Requires:         perl(Getopt::Long)
Requires:         perl(IPC::Open3)
Requires:         perl(JSON)
Requires:         perl(LWP::Simple)
Requires:         perl(Memoize)
Requires:         perl(Socket)
Requires:         perl(Sys::Hostname)
Requires:         perl(Test::More)
Requires:         perl(Time::HiRes)

%{?with_conflicts_mariadb:Conflicts: mariadb-test}
%{?with_provides_community_mysql:Provides: community-mysql-test = %community_mysql_version}
%{?with_provides_community_mysql:Provides: community-mysql-test%{?_isa} = %community_mysql_version}
%{?with_obsoletes_community_mysql:Obsoletes: community-mysql-test <= %obsolete_community_mysql_version}

%add_metadata test

%description      test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.
%endif

%prep
%autosetup -p1

# Remove bundled code that is unused (all cases in which we use the system version of the library instead)
# as required by https://docs.fedoraproject.org/en-US/packaging-guidelines/#bundling
rm -r extra/curl
rm -r extra/icu
rm -r extra/libcbor
rm -r extra/libedit
rm -r extra/libfido2
rm -r extra/protobuf
rm -r extra/tirpc
rm -r extra/zlib
rm -r extra/zstd
# Three files from the lz4 bundle tree are still needed.
# They are the 'xxhash' library with custom extension to it.
find extra/lz4 -type f ! \( -name 'xxhash.c' -o -name 'xxhash.h' -o -name 'my_xxhash.h' \) -delete

# Needed for unit tests (different from MTR tests), which we doesn't run, as they doesn't work on some architectures: #1989847
rm -r extra/googletest
rm -r extra/abseil

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE50} | tee -a mysql-test/%{skiplist}

# disable some tests failing on different architectures
%ifarch aarch64
cat %{SOURCE51} | tee -a mysql-test/%{skiplist}
%endif

%ifarch s390x
cat %{SOURCE52} | tee -a mysql-test/%{skiplist}
%endif

%ifarch ppc64le
cat %{SOURCE53} | tee -a mysql-test/%{skiplist}
%endif

echo "HEYWEAREHERE"
pwd
ls -l

cp %{SOURCE2} %{SOURCE3} %{SOURCE10} %{SOURCE11} %{SOURCE12} \
   %{SOURCE14} %{SOURCE15} %{SOURCE17} %{SOURCE18} %{SOURCE31} scripts

echo "HEYWEAREHERE"
pwd
ls scripts -l

%build
# Create an out-of-source build directory
mkdir temp
cd temp

# Ensure previous cache files are cleared to avoid conflicts
rm -rf *

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.
%cmake .. \
    -DBUILD_CONFIG=mysql_release \
    -DINSTALL_LAYOUT=RPM \
    -DWITH_ZLIB=system \
    -DDAEMON_NAME="%{daemon_name}" \
    -DDAEMON_NO_PREFIX="%{daemon_no_prefix}" \
    -DLOGFILE_RPM="%{logfile}" \
    -DPID_FILE_DIR="%{pidfiledir}" \
    -DNICE_PROJECT_NAME="MySQL" \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    -DSYSCONFDIR="%{_sysconfdir}" \
    -DSYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
    -DINSTALL_DOCDIR="/share/doc/%{majorname}" \
    -DINSTALL_DOCREADMEDIR="/share/doc/%{majorname}" \
    -DINSTALL_INCLUDEDIR=/include/mysql \
    -DINSTALL_INFODIR=/share/info \
    -DINSTALL_LIBEXECDIR=/libexec \
    -DINSTALL_LIBDIR="%{_lib}/mysql" \
    -DRPATH_LIBDIR="%{_libdir}" \
    -DINSTALL_MANDIR=/usr/share/man \
    -DINSTALL_MYSQLSHAREDIR=/usr/share/%{majorname} \
    -DINSTALL_MYSQLTESTDIR=/usr/share/mysql-test \
    -DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
    -DINSTALL_SBINDIR=/usr/bin \
    -DINSTALL_SUPPORTFILESDIR=/usr/share/%{majorname} \
    -DMYSQL_DATADIR="%{dbdatadir}" \
    -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
    -DENABLED_LOCAL_INFILE=ON \
    -DWITH_SYSTEMD=1 \
    -DSYSTEMD_SERVICE_NAME="%{daemon_name}" \
    -DSYSTEMD_PID_DIR="%{pidfiledir}" \
    -DWITH_INNODB_MEMCACHED=ON \
    -DWITH_ROUTER=OFF \
    -DWITH_SYSTEM_LIBS=ON \
    -DWITH_ZSTD=system \
    -DWITH_FIDO=%{?with_fido:system}%{!?with_fido:none} \
    -DWITH_AUTHENTICATION_FIDO=%{?with_fido:ON}%{!?with_fido:OFF} \
    -DWITH_AUTHENTICATION_KERBEROS=%{?with_kerberos:ON}%{!?with_kerberos:OFF} \
    -DWITH_AUTHENTICATION_LDAP=%{?with_ldap:ON}%{!?with_ldap:OFF} \
    -DWITH_BOOST=boost \
    -DREPRODUCIBLE_BUILD=OFF \
    -DCMAKE_C_FLAGS="%{optflags}%{?with_debug: -fno-strict-overflow -Wno-unused-result -Wno-unused-function -Wno-unused-but-set-variable}" \
    -DCMAKE_CXX_FLAGS="%{optflags}%{?with_debug: -fno-strict-overflow -Wno-unused-result -Wno-unused-function -Wno-unused-but-set-variable}" \
    -DCMAKE_EXE_LINKER_FLAGS="-pie %{build_ldflags}" \
    -DWITH_LTO=ON \
    -DTMPDIR=/var/tmp \
    -DCMAKE_C_LINK_FLAGS="%{build_ldflags}" \
    -DCMAKE_CXX_LINK_FLAGS="%{build_ldflags}" \
    -DCMAKE_SKIP_INSTALL_RPATH=YES \
    -DWITH_UNIT_TESTS=0 \
%ifnarch aarch64 s390x
    -DWITH_NUMA=ON \
%endif
%ifarch s390x
    -DUSE_LD_GOLD=OFF \
%endif
%{?with_debug: -DWITH_DEBUG=1} \
%{?with_debug: -DMYSQL_MAINTAINER_MODE=0}

# Ensure the environment variable CMAKE_VERBOSE_MAKEFILE is set to 1 for detailed output
export CMAKE_VERBOSE_MAKEFILE=1

# Print all CMake options values; "-LAH" means "List Advanced Help"
cmake -B %{_vpath_builddir} -LAH .

%cmake_build


%install
# Move to the out-of-source directory to get to Make files
echo "FIRST TEST"
pwd
#ls -l
cd temp

echo "SECOND TESTTTT"
pwd
# ls -l

echo "TESTBEFORE"
pwd
%cmake_install

# multilib support for shell scripts
# we only apply this to known Red Hat multilib arches, per bug #181335
# if %multilib_capable; then
# mv %{buildroot}%{_bindir}/mysql_config %{buildroot}%{_bindir}/mysql_config-%{__isa_bits}
# install -p -m 0755 %{_vpath_builddir}/scripts/mysql_config_multilib %{buildroot}%{_bindir}/mysql_config
# fi


pwd
# ls -l
# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also %%{name}-file-contents.patch)
install -p -m 0644 Docs/INFO_SRC %{buildroot}%{_libdir}/mysql/
install -p -m 0644 Docs/INFO_BIN %{buildroot}%{_libdir}/mysql/


mkdir -p %{buildroot}%{logfiledir}

mkdir -p %{buildroot}%{pidfiledir}
install -p -m 0755 -d %{buildroot}%{dbdatadir}
install -p -m 0750 -d %{buildroot}%{_localstatedir}/lib/mysql-files
install -p -m 0700 -d %{buildroot}%{_localstatedir}/lib/mysql-keyring

echo "TESTNEW"
%if %{with config}
install -D -p -m 0644 ../scripts/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
%endif
echo "TESTNEW1"
# install systemd unit files and scripts for handling server startup
install -D -p -m 644 ../scripts/mysql.service %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 644 ../scripts/mysql@.service %{buildroot}%{_unitdir}/%{daemon_name}@.service
install -D -p -m 0644 ../scripts/mysql.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{daemon_name}.conf
rm -r %{buildroot}%{_tmpfilesdir}/mysql.conf

echo "TESTNEW2"
#BUILDROOT: /usr/src/azl/BUILDROOT/mysql-8.4.3-1.azl3.x86_64
# echo 'MANDIR: /usr/share/man'

# helper scripts for service starting
install -D -p -m 755 ../scripts/mysql-prepare-db-dir.sh %{buildroot}%{_libexecdir}/mysql-prepare-db-dir.sh
install -p -m 755 ../scripts/mysql-wait-stop.sh %{buildroot}%{_libexecdir}/mysql-wait-stop.sh
install -p -m 755 ../scripts/mysql-check-socket.sh %{buildroot}%{_libexecdir}/mysql-check-socket.sh
install -p -m 644 ../scripts/mysql-scripts-common.sh %{buildroot}%{_libexecdir}/mysql-scripts-common.sh
install -D -p -m 0644 ../scripts/server.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/%{majorname}-server.cnf

rm %{buildroot}%{_libdir}/mysql/*.a
rm %{buildroot}%{_mandir}/man1/comp_err.1*

echo "TESTNEW4"
# Put logrotate script where it needs to be
mkdir -p %{buildroot}%{logrotateddir}
# Remove the wrong fill
rm %{buildroot}%{_datadir}/%{majorname}/mysql-log-rotate
# Install the correct one (meant for FSH layout in RPM packages)
install -D -m 0644 packaging/rpm-common/mysql.logrotate %{buildroot}%{logrotateddir}/%{daemon_name}

echo "TESTNEW5"
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/mysql" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
echo "TESTNEW6"
# for back-ward compatibility and SELinux, let's keep the mysqld in libexec
# and just create a symlink in /usr/sbin
mv %{buildroot}%{_bindir}/mysqld %{buildroot}%{_libexecdir}/mysqld
mkdir -p %{buildroot}%{_sbindir}
ln -s ../libexec/mysqld %{buildroot}%{_sbindir}/mysqld
echo "TESTNEW7"
%if %{with debug}
mv %{buildroot}%{_bindir}/mysqld-debug %{buildroot}%{_libexecdir}/mysqld
%endif
echo "TESTNEW8"
# copy additional docs into build tree so %%doc will find them
install -p -m 0644 %{SOURCE6} %{_vpath_srcdir}/%{basename:%{SOURCE6}}
install -p -m 0644 %{SOURCE7} %{_vpath_srcdir}/%{basename:%{SOURCE7}}

echo "TESTNEW9"
# /usr/src/azl/BUILDROOT/mysql-8.4.3-1.azl3.x86_64/usr/share/mysql-test/./platform-specific-tests.list
# /usr/src/azl/BUILDROOT/mysql-8.4.3-1.azl3.x86_64/usr/share/mysql-test/platform-specific-tests.list


#level=debug msg="install: '/usr/src/azl/BUILDROOT/mysql-8.4.3-1.azl3.x86_64/usr/share/mysql-test/./platform-specific-tests.list' and 
#'/usr/src/azl/BUILDROOT/mysql-8.4.3-1.azl3.x86_64/usr/share/mysql-test/platform-specific-tests.list' are the same file"

#"install: cannot stat './mysql-test/./platform-specific-tests.list': No such file or directory"

pwd

echo "LSUSR"
# ls -l usr

echo "LSSHARE"
# ls -l share

echo "LSmysql-test"
# ls -l mysql-test

# Install the list of skipped tests to be available for user runs
install -p -m 0644 ../mysql-test/./%{skiplist} %{buildroot}%{_datadir}/mysql-test

unlink %{buildroot}%{_libdir}/mysql/libmysqlclient.so
rm -r %{buildroot}%{_libdir}/mysql/libmysqlclient*.so.*
rm -r %{buildroot}%{_sysconfdir}/ld.so.conf.d

rm %{buildroot}%{_bindir}/mysql_config*
rm -r %{buildroot}%{_includedir}/mysql
rm %{buildroot}%{_datadir}/aclocal/mysql.m4
rm %{buildroot}%{_libdir}/pkgconfig/mysqlclient.pc
rm %{buildroot}%{_libdir}/mysql/libmysqlclient*.so
rm %{buildroot}%{_mandir}/man/mysql_config.1*


echo "TESTNEW11"

rm %{buildroot}%{_bindir}/{mysql,mysql_config_editor,\
mysql_plugin,mysqladmin,mysqlbinlog,\
mysqlcheck,mysqldump,mysqlpump,mysqlimport,mysqlshow,mysqlslap,my_print_defaults}
rm %{buildroot}%{_mandir}/man/{mysql,mysql_config_editor,\
mysql_plugin,mysqladmin,mysqlbinlog,\
mysqlcheck,mysqldump,mysqlpump,mysqlimport,mysqlshow,mysqlslap,my_print_defaults}.1*

echo "TESTNEW12"

mkdir -p %{buildroot}%{_sysconfdir}/my.cnf.d

#rm %{buildroot}%{_sysconfdir}/my.cnf



rm -r %{buildroot}%{_datadir}/%{majorname}/charsets

echo "TESTNEW13"

rm %{buildroot}%{_datadir}/%{majorname}/{messages_to_error_log.txt,messages_to_clients.txt}
rm -r %{buildroot}%{_datadir}/%{majorname}/{english,bulgarian,czech,danish,dutch,estonian,\
french,german,greek,hungarian,italian,japanese,korean,norwegian,norwegian-ny,\
polish,portuguese,romanian,russian,serbian,slovak,spanish,swedish,ukrainian}


echo "TESTNEW14"

rm %{buildroot}%{_bindir}/{mysql_client_test,mysqlxtest,mysqltest_safe_process,zlib_decompress}
rm -r %{buildroot}%{_datadir}/mysql-test





%check

echo "STARTCHECK"

%if %{with test}
%if %runselftest
pushd %_vpath_builddir
# Note: disabling building of unittests to workaround #1989847
#make test VERBOSE=1
pushd mysql-test
cp ../../mysql-test/%{skiplist} .

# Builds might happen at the same host, avoid collision
#   The port used is calculated as 10 * MTR_BUILD_THREAD + 10000
#   The resulting port must be between 5000 and 32767
export MTR_BUILD_THREAD=$(( $(date +%s) % 2200 ))

(
  set -ex
  cd %{buildroot}%{_datadir}/mysql-test

  export common_testsuite_arguments=" %{?with_debug:--debug-server} --parallel=auto --force --retry=2 --suite-timeout=900 --testcase-timeout=30 --skip-combinations --max-test-fail=5 --report-unstable-tests --clean-vardir --nocheck-testcases "

  # If full testsuite has already been run on this version and we don't explicitly want the full testsuite to be run
  if [[ "%{last_tested_version}" == "%{version}" ]] && [[ %{force_run_testsuite} -eq 0 ]]
  then
    # in further rebuilds only run the basic "main" suite (~800 tests)
    echo "running only base testsuite"
    perl ./mysql-test-run.pl $common_testsuite_arguments --suite=main --skip-test-list=%{skiplist}
  fi

 # If either this version wasn't marked as tested yet or I explicitly want to run the testsuite, run everything we have (~4000 test)
  if [[ "%{last_tested_version}" != "%{version}" ]] || [[ %{force_run_testsuite} -ne 0 ]]
  then
    echo "running advanced testsuite"
    perl ./mysql-test-run.pl $common_testsuite_arguments \
    %if %{ignore_testsuite_result}
      --max-test-fail=9999 || :
    %else
      --skip-test-list=%{skiplist}
    %endif
  fi

  # There might be a dangling symlink left from the testing, remove it to not be installed
  rm -r var $(readlink var)
)

popd
popd

%endif
%endif


%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{dbdatadir} -s /sbin/nologin \
  -c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :

%post server
%systemd_post %{daemon_name}.service
if [ ! -e "%{logfile}" -a ! -h "%{logfile}" ] ; then
    install /dev/null -m0640 -omysql -gmysql "%{logfile}"
fi

%preun server
%systemd_preun %{daemon_name}.service

%postun server
%systemd_postun_with_restart %{daemon_name}.service

%files

echo "FILESSTART"
pwd
echo "LETSLS"
ls ${_bindir} -l

%defattr(-,root,root)
%license LICENSE router/LICENSE.router
%doc README router/README.router
%{_bindir}/mysql
%{_bindir}/mysql_config_editor
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqldumpslow
%{_bindir}/perror

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config_editor.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/perror.1*

%files libs
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/*

%files devel
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/private/icudt73l/brkitr/*.res
%{_libdir}/private/icudt73l/brkitr/*.brk
%{_libdir}/private/icudt73l/brkitr/*.dict
%{_libdir}/private/icudt73l/unames.icu
%{_libdir}/private/icudt73l/ulayout.icu
%{_libdir}/private/icudt73l/uemoji.icu
%{_libdir}/private/icudt73l/cnvalias.icu
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
* Thu Aug 15 2024 Betty Lakes <bettylakes@microsoft.com> - 8.4.2-1
- Upgrade to 8.4.2

* Thu Feb 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.36-1
- Auto-upgrade to 8.0.36

* Mon Apr 24 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.33-1
- Auto-upgrade to 8.0.33 - address CVE-2023-21976, CVE-2023-21972, CVE-2023-21982, CVE-2023-21977, CVE-2023-21980

* Thu Feb 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.32-1
- Auto-upgrade to 8.0.32 - CVE-2023-21879 CVE-2023-21875 CVE-2023-21877 CVE-2023-21876 CVE-2023-21878 CVE-2023-21883 CVE-2023-21881 CVE-2023-21880 CVE-2023-21882 CVE-2023-21887 

* Mon Oct 24 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.31-1
- Upgrade to 8.0.31

* Thu Jun 23 2022 Henry Beberman <henry.beberman@microsoft.com> - 8.0.29-1
- Upgrade to 8.0.29 to fix 17 CVEs

* Wed Jan 26 2022 Neha Agarwal <thcrain@microsoft.com> - 8.0.28-1
- Upgrade to 8.0.28 to fix 16 CVEs

* Sat Apr 24 2021 Thomas Crain <thcrain@microsoft.com> - 8.0.24-1
- Upgrade to 8.0.24 to fix 30 CVEs
- Update source URL

* Thu Feb 11 2021 Rachel Menge <rachelmenge@microsoft.com> - 8.0.23-1
- Upgrade to 8.0.23. Fixes CVE-2020-15358.

* Thu Nov 05 2020 Rachel Menge <rachelmenge@microsoft.com> - 8.0.22-2
- Added no patch for CVE-2012-5627

* Tue Nov 03 2020 Rachel Menge <rachelmenge@microsoft.com> - 8.0.22-1
- Upgrade to 8.0.22. Fixes 40 CVES.
- Lint spec

* Tue Aug 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 8.0.21-1
- Upgrade to 8.0.21. Fixes 32 CVEs.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.0.20-2
- Added %%license line automatically

* Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> - 8.0.20-1
- Upgrade to 8.0.20. Fixes 70 CVEs.
- Update URL.
- Fix CVE-2020-2804.

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 8.0.17-1
- Update to version 8.0.17. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 8.0.14-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 22 2019 Siju Maliakkal <smaliakkal@vmware.com> - 8.0.14-1
- Upgrade to 8.0.14

* Wed Jan 02 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> - 8.0.13-1
- Upgrade to version 8.0.13
- Workaround for broken DCMAKE_BUILD_TYPE=RELEASE(Mysql Bug#92945). Revert in next version

* Mon Nov 19 2018 Ajay Kaher <akaher@vmware.com> - 8.0.12-4
- Enabling for aarch64

* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> - 8.0.12-3
- Adding BuildArch

* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> - 8.0.12-2
- Use libtirpc instead obsoleted rpc from glibc.

* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 8.0.12-1
- Update to version 8.0.12

* Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 5.7.23-1
- Update to version 5.7.23 to get it to build with gcc 7.3

* Thu Jan 25 2018 Divya Thaluru <dthaluru@vmware.com> - 5.7.20-2
- Added patch for CVE-2018-2696

* Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.7.20-1
- Update to version 5.7.20

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 5.7.18-3
- Fix typo in description

* Fri Jul 14 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.7.18-2
- Run make test in the %check section

* Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.7.18-1
- Initial packaging for Photon
