%define mstflint_unsigned_name mstflint-kernel

Summary:        Mellanox firmware burning tool
Name:           %{mstflint_unsigned_name}-signed
Version:        4.21.0
Release:        4%{?dist}
License:        GPLv2 OR BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/Mellanox/%{name}
Source0:        https://github.com/Mellanox/%{name}/releases/download/v%{version}-1/%{name}-%{version}-1.tar.gz

# set package name
%{!?_name: %global _name mstflint}

%global kver %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-devel))
%global ksrc %{_libdir}/modules/%{kver}/build
%global debug_package %{nil}
%global kernel_source() %{ksrc}
%global kernel_release() %{kver}
%global flavors_to_build default
%global install_mod_dir extra/%{_name}
%define mstflint_name %(value="%{mstflint_unsigned_name}-%{version}-%{release}"; echo "${value//[^a-zA-Z0-9_]/_}")
%define mstflint_module_name mstflint_access.ko
%define mstflint_module_path %{install_mod_dir}/%{mstflint_module_name}

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
mkdir -p %{install_mod_dir}
cd kernel
for flavor in %{flavors_to_build}; do
  export KSRC=%{kernel_source $flavor}
  export KVERSION=%{kernel_release $KSRC}
  install -d $INSTALL_MOD_PATH/lib/modules/$KVERSION/%{install_mod_dir}
  cp $PWD/obj/$flavor/%{mstflint_module_name} $INSTALL_MOD_PATH/lib/modules/$KVERSION/%{install_mod_dir}
done
cd -

%files -n %{mstflint_unsigned_name}
%defattr(-,root,root,-)
/lib/modules/%{kver}/%{install_mod_dir}/

%changelog
* Thu Mar 06 2023 Elaheh Dehghani <edehghani@microsoft.com> - 4.21.0-4
- Add mstflint driver for secure boot.
