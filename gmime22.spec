Summary:	libGMIME library
Summary(pl):	Biblioteka GMIME
Name:		gmime
Version:	1.90.0
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	http://spruce.sourceforge.net/gmime/sources/gmime-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://spruce.sourceforge.net/gmime
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gtk-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows you to manipulate MIME messages.

%description -l pl
Ta biblioteka pozwala na manipulowanie wiadomościami MIME.

%package devel
Summary:	Libraries, includes, etc to develop libgmime applications
Summary(pl):	Biblioteki, nagłówki, itp. do tworzenia programów z libgmime
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries, include files, etc you can use to develop libgmime
applications.

%description devel -l pl
Bibliotek, pliki nagłówkowe itp. potrzebne do tworzenia programów
opartych o bibliotekę gmime.

%package static
Summary:	Static gmime libraries
Summary(pl):	Statyczne biblioteki gmime
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static gmime libraries.

%description static -l pl
Statyczne biblioteki gmime.

%prep
%setup -q
%patch0 -p1

%build
rm -rf missing
%{__libtoolize}
aclocal
%{__autoconf}
#%{__automake}
CFLAGS="$CFLAGS -I /usr/X11R6/include"
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/gmime-config
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/*.sh
%attr(644,root,root) %{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
