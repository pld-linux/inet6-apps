Summary:	Inet6 Applications for Linux
Summary(pl.UTF-8):	Podstawowe aplikacje sieciowe ze wspomaganiem dla IPv6
Name:		inet6-apps
Version:	0.36
Release:	5
License:	BSD & NRL
Group:		Networking
Source0:	ftp://ftp.inner.net/pub/ipv6/%{name}-%{version}.tar.gz
# Source0-md5:	4805423bddc547ed931203cbc2998e2f
Patch0:		%{name}-config.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-ftp.patch
Patch4:		%{name}-rfc2292.patch
Patch5:		%{name}-cpp_macros.patch
BuildRequires:	bison
BuildRequires:	db3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a kit of IPv6-aware applications designed to replace many of
the basic networking programs that come with your system. Most of
these support IPv4, IPv6, and UNIX domain sockets.

%description -l pl.UTF-8
Pakiet ten zawiera podstawowe narzędzia sieciowe wspierające nowy
protokół IPv6 i jest zamiennikiem starych aplikacji takich jak
netkit-base.

%package -n ftp6
Summary:	Standard Unix FTP (file transfer protocol) client
Summary(pl.UTF-8):	Standardowy klient FTP dla Linuksa
Group:		Applications/Networking

%description -n ftp6
This provides the standard Unix command-line FTP client. FTP is the
standard Internet file transfer protocol, now with IPv6 support, which
is extremely popular for both file archives and file transfers between
individuals.

%description -n ftp6 -l pl.UTF-8
Pakiet ten zawiera standardowego klienta FTP. FTP (file transfer
protocol) jest bardzo popularny w internecie i daje możliwość np.:
ściągania oprogramowania z serwera na którym klient nie ma konta.
Klient obecnie ma wsparcie dla protokołu IPv6.

%package -n ftpd6
Summary:	Standard Unix FTP (file transfer protocol) server
Summary(pl.UTF-8):	Standardowy serwer FTP dla Linuksa
Group:		Networking/Daemons

%description -n ftpd6
This provides the standard Unix FTP server. FTP is the standard
Internet file transfer protocol, now with IPv6 support, which is
extremely popular for both file archives and file transfers between
individuals.

%description -n ftpd6 -l pl.UTF-8
Pakiet ten zawiera standardowy serwer FTP. FTP (file transfer
protocol) jest bardzo popularny w internecie i daje możliwość np.:
ściągania oprogramowania z serwera na którym klient nie ma konta.
Serwer obecnie ma wsparcie dla protokołu IPv6.

%package -n finger6
Summary:	IPv6 Finger client
Summary(pl.UTF-8):	Klient Finger
Group:		Networking/Utilities

%description -n finger6
Finger is a simple protocol which allows users to find information
about users on other machines, now with IPv6 support. This package
includes a standard finger client.

%description -n finger6 -l pl.UTF-8
Finger jest prostym protokołem który umożliwia wyszukiwanie informacji
o użytkownikach na innym serwerze, teraz ma już wsparcie dla IPv6.
Pakiet ten zawiera klienta fingera.

%package -n fingerd6
Summary:	Finger server
Summary(pl.UTF-8):	Serwer finger
Group:		Networking/Daemons

%description -n fingerd6
Finger is a simple protocol which allows users to find information
about users on other machines, now with IPv6 support. This package
includes a standard finger server. The server runs from
/etc/inetd.conf, which must be modified to disable finger requests.

%description -n fingerd6 -l pl.UTF-8
Finger jest prostym protokołem który umożliwia wyszukiwanie informacji
o użytkownikach na innym serwerze, teraz ma już wsparcie dla IPv6.
Pakiet ten zawiera serwer fingera.

%package -n ping
Summary:	ping
Summary(pl.UTF-8):	ping
Group:		Networking/Admin
Obsoletes:	iputils-ping

%description -n ping
ping.

%description -n ping -l pl.UTF-8
ping.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__make} \
	CC="%{__cc} %{rpmcflags}"

%{__make} -C ftpd \
	YACC="bison -y"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{8,5},%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT{/bin,/etc/ftpd}

install ftp/ftp $RPM_BUILD_ROOT%{_bindir}/ftp6

touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/welcome
touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/motd
touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/motd-6
touch $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/ftpusers

install ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd6
install ftpd/ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/ftpd.8

#end ftp

#begin finger
install finger/finger $RPM_BUILD_ROOT%{_bindir}/finger6
install fingerd/fingerd $RPM_BUILD_ROOT%{_sbindir}/fingerd6
#end finger

#begin inet6-apps

install ping/ping $RPM_BUILD_ROOT%{_sbindir}
install ping/ping.8 $RPM_BUILD_ROOT%{_mandir}/man8

install etc/hosts $RPM_BUILD_ROOT%{_sysconfdir}
install man/hosts.5 $RPM_BUILD_ROOT%{_mandir}/man5

install misc/{gendata,socktest} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n ftpd6
cat /etc/passwd | cut -d: -f1 | grep -v ftp >> \
	/etc/ftpd/ftpusers

%files -n ping
%defattr(644,root,root,755)
%attr(4711,root,root) %{_sbindir}/ping
%{_mandir}/man8/ping*

%files -n ftpd6
%defattr(644,root,root,755)
%dir %{_sysconfdir}/ftpd

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/welcome
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/motd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/motd-6
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/ftpusers

%attr(755,root,root) %{_sbindir}/ftpd6

%{_mandir}/man8/ftpd*

%files -n ftp6
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ftp6

%files -n finger6
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/finger6

%files -n fingerd6
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/fingerd6
