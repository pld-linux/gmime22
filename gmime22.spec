#
# Conditional build:
%bcond_without	dotnet	# without .net support
#
%ifarch i386
%undefine	with_dotnet
%endif
%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}
Summary:	GMIME library
Summary(pl.UTF-8):	Biblioteka GMIME
Name:		gmime22
Version:	2.2.27
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gmime/2.2/gmime-%{version}.tar.bz2
# Source0-md5:	16d89accbe5c79ba22e3dfabf53e3b7e
Patch0:		%{name}-link.patch
Patch1:		%{name}-dont-delay-sign.patch
URL:		http://spruce.sourceforge.net/gmime/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.12.1
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtk-doc-automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
%if %{with dotnet}
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.9.0
BuildRequires:	mono-csharp >= 1.1.16.1
%endif
Obsoletes:	gmime < 2.2.23
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows you to manipulate MIME messages.

%description -l pl.UTF-8
Ta biblioteka pozwala na manipulowanie wiadomościami MIME.

%package devel
Summary:	Header files to develop libgmime applications
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów z użyciem libgmime
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.12.1
Requires:	zlib-devel
Obsoletes:	gmime-devel < 2.2.23

%description devel
Header files develop libgmime applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem libgmime.

%package static
Summary:	Static gmime library
Summary(pl.UTF-8):	Statyczna biblioteka gmime
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	gmime-static < 2.2.23

%description static
Static gmime library.

%description static -l pl.UTF-8
Statyczna biblioteka gmime.

%package apidocs
Summary:	gmime library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gmime
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gmime library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gmime.

%package -n dotnet-gmime22-sharp
Summary:	.NET language bindings for gmime
Summary(pl.UTF-8):	Wiązania gmime dla .NET
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dotnet-gtk-sharp2 >= 2.9.0
Requires:	mono >= 1.1.16.1
Obsoletes:	dotnet-gmime-sharp < 2.2.23

%description -n dotnet-gmime22-sharp
.NET language bindings for gmime.

%description -n dotnet-gmime22-sharp -l pl.UTF-8
Wiązania gmime dla .NET.

%package -n dotnet-gmime22-sharp-devel
Summary:	Development part of dotnet-gmime-sharp
Summary(pl.UTF-8):	Część dla programistów dotnet-gmime-sharp
Group:		Development/Libraries
Requires:	dotnet-%{name}-sharp = %{version}-%{release}
Obsoletes:	dotnet-gmime-sharp-devel < 2.2.23

%description -n dotnet-gmime22-sharp-devel
Development part of dotnet-gmime-sharp.

%description -n dotnet-gmime22-sharp-devel -l pl.UTF-8
Część dla programistów dotnet-gmime-sharp.

%prep
%setup -q -n gmime-%{version}
%patch0 -p1
%patch1 -p1

%build
touch config.rpath
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-largefile \
	--%{?with_dotnet:enable}%{!?with_dotnet:disable}-mono \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

rm -f $RPM_BUILD_ROOT%{_bindir}/uu{de,en}code

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libgmime-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgmime-2.0.so.2

%files devel
%defattr(644,root,root,755)
%doc PORTING
%attr(755,root,root) %{_bindir}/gmime-config
%attr(755,root,root) %{_libdir}/libgmime-2.0.so
%{_libdir}/libgmime-2.0.la
%attr(755,root,root) %{_libdir}/gmimeConf.sh
%{_pkgconfigdir}/gmime-2.0.pc
%{_includedir}/gmime-2.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libgmime-2.0.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gmime

%if %{with dotnet}
%files -n dotnet-gmime22-sharp
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gac/gmime-sharp

%files -n dotnet-gmime22-sharp-devel
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gmime-sharp
%{_datadir}/gapi-2.0/gmime-api.xml
%{_pkgconfigdir}/gmime-sharp.pc
%endif
