%define isal_version 2.30.0

Summary:        Storage Performance Development Kit
Name:           spdk
Version:        22.09
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://spdk.io
Source0:        https://github.com/spdk/spdk/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/intel/isa-l/archive/refs/tags/v%{isal_version}.tar.gz#/isa-l-%{isal_version}.tar.gz
Patch0:         0001-link-with-libarchive-on-Linux.patch
ExclusiveArch:  x86_64 aarch64
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  dpdk-devel
BuildRequires:  isa-l-devel
BuildRequires:  libaio-devel
BuildRequires:  libarchive-devel
BuildRequires:  ncurses-devel
BuildRequires:  numactl-devel
BuildRequires:  sed
BuildRequires:  zlib-devel
Requires:       libaio
Requires:       libarchive
Requires:       ncurses
Requires:       numactl
Requires:       zlib
Requires:       dpdk

%description
The Storage Performance Development Kit (SPDK) provides a set of tools and libraries for writing high performance, scalable, user-mode storage applications. It achieves high performance by moving all of the necessary drivers into userspace and operating in a polled mode instead of relying on interrupts, which avoids kernel context switches and eliminates interrupt handling overhead.

%package devel
Summary:        Storage Performance Development Kit development files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the Storage Performance Development Kit (SPDK) package.

%prep
%autosetup -p1 -n %{name}-%{version} -a1

mv isa-l isa-l.orig
ln -s isa-l-%{isal_version} isa-l

%build
./configure \
    --prefix=/usr \
    --disable-unit-tests \
    --disable-tests \
    --disable-examples \
    --disable-apps \
    --with-shared \
    --with-dpdk=/usr
%make_build

%install
%make_install

%files
%attr(0644,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so*

%files devel
%attr(0644,root,root)
%{_includedir}/*
%{_libdir}/*.a


%changelog
* Wed Oct 05 2022 Taylor Hope <tayloh@microsoft.com> - 22.09-2
- Added shared libraries

* Mon Oct 03 2022 Sriram Nambakam <snambakam@microsoft.com> - 22.09-1
- Initial CBL-Mariner Spec
- License verified
