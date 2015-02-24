#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

Summary:	QtIOCompressor is a QIODevice that compresses data streams
Name:		QtIOCompressor
Version:	2.3
Release:	2
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtiocompressor-%{version}_1-opensource.tar.gz
# Source0-md5:	73bbde56cf705602b4f180b379756a40
Source1:	qtiocompressor.prf
Patch0:		libs.patch
URL:		http://doc.qt.digia.com/solutions/4/qtiocompressor/qtiocompressor.html
BuildRequires:	sed >= 4.0
%if %{with qt4}
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt4dir	%{_datadir}/qt4
%define		qt5dir	%{_libdir}/qt5

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

%package -n Qt5IOCompressor
Summary:	QtIOCompressor is a QIODevice that compresses data streams
Group:		Libraries

%description -n Qt5IOCompressor
The class works on top of a QIODevice subclass, compressing data
before it is written and decompressing it when it is read.

Since QtIOCompressor works on streams, it does not have to see the
entire data set before compressing or decompressing it. This can
reduce the memory requirements when working on large data sets.

%package -n Qt5IOCompressor-devel
Summary:	Development files for Qt5IOCompressor
Group:		Development/Libraries
Requires:	Qt5IOCompressor = %{version}-%{release}
Requires:	qt5-build
Requires:	qt5-qmake

%description -n Qt5IOCompressor-devel
This package contains libraries and header files for developing
applications that use Qt5IOCompressor.

%prep
%setup -q -n qtiocompressor-%{version}_1-opensource
%patch0 -p1

# skip building examples
%{__sed} -i -e '/^SUBDIRS+=examples$/d' *.pro

touch .licenseAccepted

set -- .??* *
install -d build-qt{4,5}
cp -al "$@" build-qt4
cp -al "$@" build-qt5

%{__sed} -i -e 's/QtSolutions/Qt5Solutions/' build-qt5/common.pri

%build
%if %{with qt4}
cd build-qt4
# Does not use GNU configure
./configure -library
qmake-qt4
%{__make}
cd ..
%endif

%if %{with qt5}
cd build-qt5
./configure -library
qmake-qt5
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
cd build-qt4
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt4/QtSolutions,%{qt4dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtiocompressor.h src/QtIOCompressor $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt4dir}/mkspecs/features
cd ..
%endif

%if %{with qt5}
cd build-qt5
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt5/QtSolutions,%{qt5dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtiocompressor.h src/QtIOCompressor $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt5dir}/mkspecs/features
cd ..
%endif

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

%if %{with qt5}
%files -n Qt5IOCompressor
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%attr(755,root,root) %{_libdir}/libQt5Solutions_IOCompressor-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Solutions_IOCompressor-%{version}.so.1

%files -n Qt5IOCompressor-devel
%defattr(644,root,root,755)
%doc doc examples
%{_libdir}/libQt5Solutions_IOCompressor-%{version}.so
%{qt5dir}/mkspecs/features/qtiocompressor.prf
%{_includedir}/qt5/QtSolutions/QtIOCompressor
%{_includedir}/qt5/QtSolutions/qtiocompressor.h
%endif
