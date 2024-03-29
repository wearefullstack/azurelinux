# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}
 
Name:           ocaml-augeas
Version:        0.6
Release:        31%{?dist}
Summary:        OCaml bindings for Augeas configuration API
License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
 
URL:            https://people.redhat.com/~rjones/augeas/files/
Source0:        https://people.redhat.com/~rjones/augeas/files/%{name}-%{version}.tar.gz
Source1:        ocaml_files.py
Source2:        macros.ocaml-rpm
 
# Upstream patch to enable debuginfo.
#Patch1:         0001-Use-ocamlopt-g-option.patch
# Const-correctness fix for OCaml 4.09+
#Patch2:         0002-caml_named_value-returns-const-value-pointer-in-OCam.patch
 
BuildRequires:  make
BuildRequires:  ocaml >= 3.09.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
#BuildRequires:  ocaml-rpm-macros
BuildRequires:  augeas-devel >= 0.1.0
 
 
%description
Augeas is a unified system for editing arbitrary configuration
files. This provides complete OCaml bindings for Augeas.
 
 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
 
%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.
 
 
%prep
%autosetup -p1
 
# Pass -g to ocamlmklib
sed -i 's/ocamlmklib/& -g/' Makefile.in

cp -v %{SOURCE1} %{_rpmconfigdir}/azl
cp -v %{SOURCE2} %{_rpmmacrodir}/
 
%build
export CFLAGS="$CFLAGS -Wno-discarded-qualifiers"
export CXXFLAGS="$CXXFLAGS -Wno-discarded-qualifiers"
export FCFLAGS="$FCFLAGS -Wno-discarded-qualifiers"

%configure
%ifarch %{ocaml_native_compiler}
make
%else
make mlaugeas.cma test_augeas
%endif
make doc
 
 
%check
make check
 
 
%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
 
# The upstream 'make install' rule is missing '*.so' and distributes
# '*.cmi' instead of just the augeas.cmi file.  Temporary fix:
#make install
%ifarch %{ocaml_native_compiler}
ocamlfind install augeas META *.mli *.cmx *.cma *.cmxa *.a augeas.cmi *.so
%else
ocamlfind install augeas META *.mli *.cma *.a augeas.cmi *.so
%endif
 
%ocaml_files
 
%files -f .ofiles
%license COPYING.LIB
 
#time="2024-03-29T01:08:26Z" level=debug msg="error: Could not open %files file /usr/src/azl/BUILD/ocaml-augeas-0.6/.ofiles: No such file or directory"
 
%files devel -f .ofiles-devel
%doc html
 
 
%changelog
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
