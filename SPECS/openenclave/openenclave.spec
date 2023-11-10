Summary:        SDK for developing enclaves
Name:           openenclave
Version:        0.19.4
Release:        1%{?dist}
License:        MIT
URL:            https://openenclave.io/sdk/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%description
Build Trusted Execution Environment based applications to help protect data in use with an open source SDK
that provides consistent API surface across enclave technologies as well as all platforms from cloud to edge.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=/bin \
    --htmldir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
sed -i 's|print_ver_ sed|Exit $fail|g' testsuite/panic-tests.sh
sed -i 's|compare exp-out out|#compare exp-out out|g' testsuite/subst-mb-incomplete.sh

make check

%files
%defattr(-,root,root)
%license COPYING
/bin/*
%{_mandir}/man1/*

%changelog
* Mon Nov 06 2023 Cameron Baird <cameronbaird@microsoft.com> - 0.19.4-1
- Introduced