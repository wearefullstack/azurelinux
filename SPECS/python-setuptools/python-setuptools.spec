%global debug_package %{nil}
%define python3_majmin 3.12

Summary:        Easily build and distribute Python packages
Name:           python-setuptools
Version:        69.0.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://pypi.python.org/pypi/setuptools
Source0:        https://pypi.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz

%description
Setuptools is a fully-featured, actively-maintained, and stable library designed to facilitate packaging Python projects.

%package -n python3-setuptools
Summary:        Easily download, build, install, upgrade, and uninstall Python packages

Requires:       python3
# Early builds of Azure Linux 3.0 included python3-setuptools with the python3.spec. Obsolete to prevent build conflicts.
Obsoletes:      python3-setuptools <= 3.9.14
BuildArch:      noarch

Provides:       python3dist(setuptools) = %{version}-%{release}
Provides:       python%{python3_majmin}dist(setuptools) = %{version}-%{release}

#Provides: bundled(python3dist(importlib-metadata)) = 6
#Provides: bundled(python3dist(importlib-resources)) = 5.10.2
#Provides: bundled(python3dist(jaraco-text)) = 3.7
#Provides: bundled(python3dist(more-itertools)) = 8.8
#Provides: bundled(python3dist(ordered-set)) = 3.1.1
#Provides: bundled(python3dist(packaging)) = 23
#Provides: bundled(python3dist(platformdirs)) = 2.6.2
#Provides: bundled(python3dist(tomli)) = 2.0.1
#Provides: bundled(python3dist(typing-extensions)) = 4.0.1
#Provides: bundled(python3dist(typing-extensions)) = 4.4
#Provides: bundled(python3dist(zipp)) = 3.7

%description -n python3-setuptools
Setuptools is a fully-featured, actively-maintained, and stable library designed to facilitate packaging Python projects.

%prep
%autosetup -n setuptools-%{version}

%build
pip3 wheel -w dist --no-cache-dir --no-build-isolation --no-deps $PWD

%install
pip3 install --no-cache-dir --no-index --ignore-installed --root %{buildroot} \
    --no-user --find-links=dist setuptools

# add path file pointing to distutils
cat > %{python3_sitelib}/distutils-precedence.pth <<- "EOF"
import os; var = 'SETUPTOOLS_USE_DISTUTILS'; enabled = os.environ.get(var, 'local') == 'local'; enabled and __import__('_distutils_hack').add_shim();
EOF

%files -n python3-setuptools
%defattr(-,root,root,755)
%{python3_sitelib}/distutils-precedence.pth
%{python3_sitelib}/pkg_resources/*
%{python3_sitelib}/setuptools/*
%{python3_sitelib}/_distutils_hack/
%{python3_sitelib}/setuptools-%{version}.dist-info/*

%changelog
* Tue Feb 13 2024 Andrew Phelps anphel@microsoft.com - 69.0.3-1
- License verified
- Original version for CBL-Mariner
