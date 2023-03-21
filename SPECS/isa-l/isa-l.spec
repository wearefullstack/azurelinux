Summary:        Intel Intelligent Storage Acceleration Library
Name:           isa-l
Version:        2.30.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://spdk.io
Source0:        https://github.com/intel/isa-l/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  yasm

%description
ISA-L is a collection of optimized low-level functions targeting storage applications.

%package devel
Summary:        Development Kit for ISA-L
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the Intel Intelligent Storage Acceleration Library.

%package docs
Summary:        Documentation for ISA-L
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description docs
This package contains the man pages and documentation for the Intel Intelligent Storage Acceleration Library.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
autoreconf -vif ..
../configure
%make_build
popd

%install
%make_install -C %{_target_platform}

%files
%attr(0755,root,root) %{_bindir}/igzip
%attr(0644,root,root)
%{_libdir}/*.so*
%{_libdir}/pkgconfig/libisal.pc

%files devel
%attr(0644,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la

%files docs
%attr(0644,root,root)
%{_mandir}/man1/igzip.1.gz

%changelog
* Mon Oct 03 2022 Sriram Nambakam <snambakam@microsoft.com> - 2.30.0-1
- Initial CBL-Mariner Spec
- License verified
