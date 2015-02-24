Summary:	QtIOCompressor is a QIODevice that compresses data streams
Name:		QtIOCompressor
Version:	2.3
Release:	1
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtiocompressor-%{version}_1-opensource.tar.gz
# Source0-md5:	73bbde56cf705602b4f180b379756a40
Source1:	qtiocompressor.prf
Patch0:		libs.patch
URL:		http://doc.qt.digia.com/solutions/4/qtiocompressor/qtiocompressor.html
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt4dir	%{_datadir}/qt4

%description
The class works on top of a QIODevice subclass, compressing data
before it is written and decompressing it when it is read.

Since QtIOCompressor works on streams, it does not have to see the
entire data set before compressing or decompressing it. This can
reduce the memory requirements when working on large data sets.

%package devel
Summary:	Development files for QtIOCompressor
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-build
Requires:	qt4-qmake

%description devel
This package contains libraries and header files for developing
applications that use QtIOCompressor.

%prep
%setup -q -n qtiocompressor-%{version}_1-opensource
%patch0 -p1

# skip building examples
%{__sed} -i -e '/^SUBDIRS+=examples$/d' *.pro

%build
touch .licenseAccepted
# Does not use GNU configure
./configure \
	-library
qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt4/QtSolutions,%{qt4dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtiocompressor.h src/QtIOCompressor $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt4dir}/mkspecs/features

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_IOCompressor-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_IOCompressor-%{version}.so.1

%files devel
%defattr(644,root,root,755)
%doc doc examples
%{_libdir}/libQtSolutions_IOCompressor-%{version}.so
%{qt4dir}/mkspecs/features/qtiocompressor.prf
%{_includedir}/qt4/QtSolutions/QtIOCompressor
%{_includedir}/qt4/QtSolutions/qtiocompressor.h
