Summary:	Inet6 Applications for Linux
Summary(pl):	Podstawowe aplikacje sieciowe ze wspomaganiem dla IPv6
Name:		inet6-apps
Version:	0.36
Release:	5
License:	BSD & NRL
Source0:	ftp://ftp.inner.net/pub/ipv6/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-ftp.patch
Patch4:		%{name}-rfc2292.patch
Patch5:		%{name}-cpp_macros.patch
Group:		Networking
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	db3-devel

%description
This is a kit of IPv6-aware applications designed to replace many of
the basic networking programs that come with your system. Most of
these support IPv4, IPv6, and UNIX domain sockets.

%description -l pl
Pakiet ten zawiera podstawowe narzêdzia sieciowe wspieraj±ce nowy
protokó³ IPv6 i jest zamiennikiem starych aplikacji takich jak
netkit-base.

%package -n	ftp6
Summary:	Standard Unix ftp (file transfer protocol) client
Summary(pl):	Standardowy klient ftp dla Linuxa
Group:		Applications/Networking

%description -n ftp6
This provides the standard Unix command-line ftp client. Ftp is the
standard Internet file transfer protocol, now with IPv6 support, which
is extremely popular for both file archives and file transfers between
individuals.

%description -n ftp6 -l pl
Pakiet ten zawiera standardowego klienta ftp. Ftp (file transfer
protocol) jest bardzo popularny w internecie i daje mo¿liwo¶æ np.:
¶ci±gania oprogramowania z serwera na którym klient nie ma konta.
Klient obecnie ma wspomaganie dla protoko³u IPv6

%package -n	ftpd6
Summary:	Standard Unix ftp (file transfer protocol) server
Summary(pl):	Standardowy serwer ftp dla Linuxa
Group:		Networking/Daemons

%description -n ftpd6
This provides the standard Unix ftp server. Ftp is the standard
Internet file transfer protocol, now with IPv6 support, which is
extremely popular for both file archives and file transfers between
individuals.

%description -n ftpd6 -l pl
Pakiet ten zawiera standardowy server ftp. Ftp (file transfer
protocol) jest bardzo popularny w internecie i daje mo¿liwo¶æ np.:
¶ci±gania oprogramowania z serwera na którym klient nie ma konta.
Serwer obecnie ma wspomaganie dla protoko³u IPv6

%package -n	finger6
Summary:	IPv6 Finger client
Summary(pl):	Klient Finger
Group:		Networking/Utilities

%description -n finger6
Finger is a simple protocol which allows users to find information
about users on other machines, now with IPv6 support. This package
includes a standard finger client.

%description -n finger6 -l pl
Finger jest prostym protoko³em który umo¿liwia wyszukiwanie iformacji
o u¿ytkownikach na innym serwerze, teraz ma ju¿ wspomaganie dla IPv6.
Pakiet ten zawiera klienta fingera.

%package -n	fingerd6
Summary:	Finger server
Summary(pl):	Serwer finger
Group:		Networking/Daemons

%description -n fingerd6
Finger is a simple protocol which allows users to find information
about users on other machines, now with IPv6 support. This package
includes a standard finger server. The server runs from
/etc/inetd.conf, which must be modified to disable finger requests.

%description -n fingerd6 -l pl
Finger jest prostym protoko³em który umo¿liwia wyszukiwanie iformacji
o u¿ytkownikach na innym serwerze, teraz ma ju¿ wspomaganie dla IPv6.
Pakiet ten zawiera serwer fingera.

%package -n	ping
Summary:	ping
Summary(pl):	ping
Group:		Networking/Admin
Obsoletes:	iputils-ping

%description -n ping
ping.

%description -n ping -l pl
ping.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__make} CC="%{__cc} %{rpmcflags}"
%{__make} -C ftpd YACC="bison -y"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man{8,5},%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT/{bin,etc/ftpd}

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

install ping/ping $RPM_BUILD_ROOT/%{_sbindir}
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

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ftpd/welcome
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ftpd/motd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ftpd/motd-6
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ftpd/ftpusers

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
