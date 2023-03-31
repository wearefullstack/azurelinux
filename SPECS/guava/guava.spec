%bcond_with bootstrap
#
# spec file for package guava
#
# Copyright (c) 2019 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Name:           guava
Version:        30.1
Release:        1%{?dist}
Summary:        Google Core Libraries for Java
License:        Apache-2.0 AND CC0-1.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://github.com/google/guava
Source0:        https://github.com/google/guava/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1:         0001-Remove-multi-line-annotations.patch

BuildRequires:  javapackages-local-bootstrap
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
%endif
BuildRequires:  msopenjdk-11

Provides:       mvn(com.google.guava:guava)
BuildArch:      noarch

%description
Guava is a suite of core and expanded libraries that include
utility classes, Google's collections, io classes, and much
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%{?javadoc_package}

%package testlib
Summary:        The guava-testlib artifact
Group:          Development/Libraries/Java

%description testlib
guava-testlib provides additional functionality for conveninent unit testing

%prep
%setup -q
 
find . -name '*.jar' -delete
 
%pom_remove_parent guava-bom
 
%pom_disable_module guava-gwt
%pom_disable_module guava-tests
 
%pom_xpath_inject pom:modules "<module>futures/failureaccess</module>"
%pom_xpath_inject pom:parent "<relativePath>../..</relativePath>" futures/failureaccess
%pom_xpath_set pom:parent/pom:version %{version}-jre futures/failureaccess
 
%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Downloads JDK source for doc generation
%pom_remove_plugin :maven-dependency-plugin guava
 
%pom_remove_dep :caliper guava-tests
 
%mvn_package :guava-parent guava
 
# javadoc generation fails due to strict doclint in JDK 1.8.0_45
%pom_remove_plugin -r :maven-javadoc-plugin
 
%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml
 
%pom_remove_dep -r :error_prone_annotations
%pom_remove_dep -r :j2objc-annotations
%pom_remove_dep -r org.checkerframework:
%pom_remove_dep -r :listenablefuture
 
annotations=$(
    find -name '*.java' \
    | xargs fgrep -h \
        -e 'import com.google.j2objc.annotations' \
        -e 'import com.google.errorprone.annotation' \
        -e 'import com.google.errorprone.annotations' \
        -e 'import com.google.common.annotations' \
        -e 'import org.codehaus.mojo.animal_sniffer' \
        -e 'import org.checkerframework' \
    | sort -u \
    | sed 's/.*\.\([^.]*\);/\1/' \
    | paste -sd\|
)
 
# guava started using quite a few annotation libraries for code quality, which
# we don't have. This ugly regex is supposed to remove their usage from the code
find -name '*.java' | xargs sed -ri \
    "s/^import .*\.($annotations);//;s/@($annotations)"'\>\s*(\((("[^"]*")|([^)]*))\))?//g'
 
%patch1 -p1
 
%mvn_package "com.google.guava:failureaccess" guava
 
%mvn_package "com.google.guava:guava-bom" __noinstall

 
%build
# Tests fail on Koji due to insufficient memory,
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332971
%mvn_build -s -f
 
%install
%mvn_install
 
%files -f .mfiles-guava
%doc CONTRIBUTORS README*
%license COPYING
 
%files testlib -f .mfiles-guava-testlib

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 25.0-6
- Moved from extended to core
- License verified
- Fixing maven provides

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 25.0-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 25.0-4.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Dec  4 2019 Fridrich Strba <fstrba@suse.com>
- Avoid version-less dependencies that can cause problems with
  some tools
* Fri Nov 22 2019 Fridrich Strba <fstrba@suse.com>
- Build the package with ant in order to prevent build cycles
  * using a generated and customized ant build system
* Thu Oct 10 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * guava-25.0-java8compat.patch
    + Avoid callingoverridden methods with covariant return types
    for java.nio.ByteBuffer and java.nio.CharBuffer, which were
    introduced in Java 9
    + This allows us to produce with Java >= 9 binaries that are
    compatible with Java 8
* Fri Apr 12 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of guava 25.0
