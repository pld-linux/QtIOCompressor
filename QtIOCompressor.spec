#
# Conditional build:
%bcond_without	qt4	# Qt4 based library
%bcond_without	qt5	# Qt5 based library

Summary:	QtIOCompressor - a QIODevice that compresses data streams
Summary(pl.UTF-8):	QtIOCompressor - QIODevice kompresujące strumienie danych
Name:		QtIOCompressor
Version:	2.3
Release:	4
License:	GPL v3 or LGPL v2 with Nokia Qt LGPL exception v1.1
Group:		Libraries
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtiocompressor-%{version}_1-opensource.tar.gz
# Source0-md5:	73bbde56cf705602b4f180b379756a40
Source1:	qtiocompressor.prf
Patch0:		libs.patch
Patch1:		%{name}-qmake.patch
URL:		http://doc.qt.digia.com/solutions/4/qtiocompressor/qtiocompressor.html
BuildRequires:	sed >= 4.0
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-qmake >= 4
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5.5
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt4mkspecsdir	%{_datadir}/qt4/mkspecs
%define		qt5mkspecsdir	%{_libdir}/qt5/mkspecs

%description
The class works on top of a QIODevice subclass, compressing data
before it is written and decompressing it when it is read.

Since QtIOCompressor works on streams, it does not have to see the
entire data set before compressing or decompressing it. This can
reduce the memory requirements when working on large data sets.

%description -l pl.UTF-8
Klasa działająca ponad podklasą QIODevice, kompresująca dane zanim
są zapisywane i dekompresująca przy odczycie.

Ponieważ QtIOCompressor działa na strumieniach, nie musi widzieć
całego zbioru danych przed kompresją czy dekompresją. Może to
zmniejszyć wymagania pamięciowe przy pracy z dużą ilością danych.

%package devel
Summary:	Development files for QtIOCompressor
Summary(pl.UTF-8):	Pliki programistyczne biblioteki QtIOCompressor
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4

%description devel
This package contains the header files for developing applications
that use QtIOCompressor.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
korzystających z biblioteki QtIOCompressor.

%package -n Qt5IOCompressor
Summary:	Qt5IOCompressor - a QIODevice that compresses data streams
Summary(pl.UTF-8):	Qt5IOCompressor - QIODevice kompresujące strumienie danych
Group:		Libraries

%description -n Qt5IOCompressor
The class works on top of a QIODevice subclass, compressing data
before it is written and decompressing it when it is read.

Since QtIOCompressor works on streams, it does not have to see the
entire data set before compressing or decompressing it. This can
reduce the memory requirements when working on large data sets.

%description -n Qt5IOCompressor -l pl.UTF-8
Klasa działająca ponad podklasą QIODevice, kompresująca dane zanim
są zapisywane i dekompresująca przy odczycie.

Ponieważ QtIOCompressor działa na strumieniach, nie musi widzieć
całego zbioru danych przed kompresją czy dekompresją. Może to
zmniejszyć wymagania pamięciowe przy pracy z dużą ilością danych.

%package -n Qt5IOCompressor-devel
Summary:	Development files for Qt5IOCompressor
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Qt5IOCompressor
Group:		Development/Libraries
Requires:	Qt5Core-devel >= 5
Requires:	Qt5IOCompressor = %{version}-%{release}

%description -n Qt5IOCompressor-devel
This package contains the header files for developing applications
that use Qt5IOCompressor.

%description -n Qt5IOCompressor-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
korzystających z biblioteki Qt5IOCompressor.

%prep
%setup -q -n qtiocompressor-%{version}_1-opensource
%patch0 -p1
%patch1 -p1

# skip building examples
%{__sed} -i -e '/^SUBDIRS+=examples$/d' *.pro

touch .licenseAccepted

%build
# Does not use GNU configure
./configure -library

%if %{with qt4}
install -d build-qt4
cd build-qt4
qmake-qt4 ../qtiocompressor.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}" \
	INSTALL_LIBDIR=%{_libdir}
%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
qmake-qt5 ../qtiocompressor.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}" \
	INSTALL_LIBDIR=%{_libdir}
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
%{__make} -C build-qt4 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_includedir}/qt4/QtSolutions,%{qt4mkspecsdir}/features}
cp -p src/qtiocompressor.h src/QtIOCompressor $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt4mkspecsdir}/features

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQtSolutions_*.so.1.0
%endif

%if %{with qt5}
%{__make} -C build-qt5 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_includedir}/qt5/QtSolutions,%{qt5mkspecsdir}/features}
cp -p src/qtiocompressor.h src/QtIOCompressor $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{qt5mkspecsdir}/features

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5Solutions_*.so.1.0
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	-n Qt5IOCompressor -p /sbin/ldconfig
%postun	-n Qt5IOCompressor -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_IOCompressor-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_IOCompressor-%{version}.so.1

%files devel
%defattr(644,root,root,755)
%doc doc examples
%attr(755,root,root) %{_libdir}/libQtSolutions_IOCompressor-%{version}.so
%{qt4mkspecsdir}/features/qtiocompressor.prf
%{_includedir}/qt4/QtSolutions/QtIOCompressor
%{_includedir}/qt4/QtSolutions/qtiocompressor.h

%if %{with qt5}
%files -n Qt5IOCompressor
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt README.TXT
%attr(755,root,root) %{_libdir}/libQt5Solutions_IOCompressor-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Solutions_IOCompressor-%{version}.so.1

%files -n Qt5IOCompressor-devel
%defattr(644,root,root,755)
%doc doc examples
%attr(755,root,root) %{_libdir}/libQt5Solutions_IOCompressor-%{version}.so
%{qt5mkspecsdir}/features/qtiocompressor.prf
%{_includedir}/qt5/QtSolutions/QtIOCompressor
%{_includedir}/qt5/QtSolutions/qtiocompressor.h
%endif
