%bcond_without bootstrap
 
%global pkg_version     11b

Summary:        LALR parser generator for Java
Name:           java-cup
Version:        0.11b
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www2.cs.tum.edu/projects/cup/
BuildArch:      noarch
 
# https://versioncontrolseidl.in.tum.de/parsergenerators/cup/-/tree/master/
Source0:        java-cup-%{version}.tar.gz
# Add OSGi manifests
Source1:        %{name}-MANIFEST.MF
Source2:        %{name}-runtime-MANIFEST.MF
 
Patch0:         %{name}-build.patch
 
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  jflex
BuildRequires:  java-cup
%endif

# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools

%description
%{name} is a LALR Parser Generator for Java

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
Javadoc for %{name}

%package manual
Summary:        Documentation for %{name}

%description manual
Documentation for %{name}.

%prep
%setup -q
%patch0 -b .build

sed -i '/<javac/s/1.5/1.7/g' build.xml

# remove all binary files
find -name "*.class" -delete

%mvn_file ':{*}' @1

# remove prebuilt JFlex
rm -rf %{name}-%{version}/bin/JFlex.jar

# remove prebuilt %{name}, if not bootstrapping
rm -rf %{name}-%{version}/bin/java-cup-11.jar

%build
export CLASSPATH=$(build-classpath %{name} %{name}-runtime jflex)

%ant -Dcupversion=20150326 -Dsvnversion=65
find -name parser.cup -delete
%ant javadoc

# inject OSGi manifests
jar ufm dist/java-cup-%{pkg_version}.jar %{SOURCE1}
jar ufm dist/java-cup-%{pkg_version}-runtime.jar %{SOURCE2}

%install
%mvn_artifact %{name}:%{name}:%{version} dist/java-cup-%{pkg_version}.jar
%mvn_artifact %{name}:%{name}-runtime:%{version} dist/java-cup-%{pkg_version}-runtime.jar

%mvn_install -J dist/javadoc

# wrapper script for direct execution
%jpackage_script %{name}.Main "" "" %{name} cup true

%files -f .mfiles
%{_bindir}/cup
%doc changelog.txt
%license licence.txt

%files manual
%doc manual.html
%license licence.txt

%files javadoc -f .mfiles-javadoc
%license licence.txt

%changelog
* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-32
- Fixing source URL.

* Thu Mar 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.11-31
- separate into bootstrap and non-bootstrap specs
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-30
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 0.11-29.7
- Provide bootstrap version of this package.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 0.11-29.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Turn on bootstrap mode.

* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xml-commons-apis xml-commons-resolver xalan-j2
  and xerces-j2 in order to solve build cycle
* Fri Sep 15 2017 fstrba@suse.com
- Do not depend on java-gcj-compat
- Fix build with jdk9: specify source and target 1.6
* Thu Aug 29 2013 mvyskocil@suse.com
- Add conflicts for each variant
- Sync .changes
- Drop weird jpackage-prepare script and use standard pre_checkin.sh
* Fri Aug 23 2013 mvyskocil@suse.com
- Disable build of javadoc
  * drop java-cup-javadoc.patch
* Fri Jan 25 2013 coolo@suse.com
- sync licenses
* Mon Jun  4 2012 cfarrell@suse.com
- license update: HPND
  SPDX syntax
* Mon Nov  8 2010 mvyskocil@suse.cz
- Build ignore xml-comons-jax-1.3-apis
* Mon May 11 2009 mvyskocil@suse.cz
- Fixed bnc#501635: Added a lincense file
* Tue May  5 2009 mvyskocil@suse.cz
- Build using gcj (for proper bootstrap of openjdk)
* Wed Apr 29 2009 mvyskocil@suse.cz
- Initial packaging of java-cup-bootstrap 0.11 in SUSE (from jpp5)
