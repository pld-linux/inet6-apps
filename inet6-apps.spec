Summary:	Inet6 Applications for Linux
Summary(pl):	Podstawowe aplikacje sieciowe ze wspomaganiem dla IPv6
Name:		inet6-apps
Version:	0.36
Release:	1
Copyright:	BSD & NRL
Source0:	ftp://ftp.inner.net/pub/ipv6/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
Patch1:		%{name}-paths.patch
Group:		Networking
Group(pl):	Sieci
Buildroot:	/tmp/%{name}-%{version}-root

%description
This is a kit of IPv6-aware applications designed to replace many of the
basic networking programs that come with your system. Most of these support
IPv4, IPv6, and UNIX domain sockets. 

%description -l pl
Pakiet ten zawiera podstawowe narzêdzia sieciowe wspieraj±ce nowy protokó³
IPv6 i jest zamiennikiem starych aplikacji takich jak netkit-base.

%package -n ftp
Summary:	Standard Unix ftp (file transfer protocol) client
Summary(pl):	Standardowy klient ftp dla Linuxa
Group:		Networking
Group(pl):	Sieci
Requires:	%{name} = %{version}

%description -n ftp
This provides the standard Unix command-line ftp client. Ftp 
is the standard Internet file transfer protocol, now with IPv6 support,
which is extremely popular for both file archives and file transfers 
between individuals.

%description -n ftp -l pl
Pakiet ten zawiera standardowego klienta ftp. Ftp 
(file transfer protocol) jest bardzo popularny w internecie i daje mo¿liwo¶æ
np.: ¶ci±gania oprogramowania z serwera na którym klient nie ma konta.
Klient obecnie ma wspomaganie dla protoko³u IPv6

%package -n ftpd
Summary:	Standard Unix ftp (file transfer protocol) server
Summary(pl):	Standardowy serwer ftp dla Linuxa
Group:		Networking/Daemons
Group(pl):	Sieci/Serwery
Requires:	%{name} = %{version}

%description -n ftpd
This provides the standard Unix ftp server. Ftp 
is the standard Internet file transfer protocol, now with IPv6 support,
which is extremely popular for both file archives and file transfers 
between individuals.

%description -n ftpd -l pl
Pakiet ten zawiera standardowy server ftp. Ftp 
(file transfer protocol) jest bardzo popularny w internecie i daje mo¿liwo¶æ
np.: ¶ci±gania oprogramowania z serwera na którym klient nie ma konta.
Serwer obecnie ma wspomaganie dla protoko³u IPv6

%package -n finger
Summary:	Finger client
Summary(pl):	Klient Finger 
Group:		Networking
Group(pl):	Sieci

%description -n finger
Finger is a simple protocol which allows users to find information about
users on other machines, now with IPv6 support. This package includes a 
standard finger client. The server runs from /etc/inetd.conf, 
which must be modified to disable finger requests.

%description -n finger -l pl
Finger jest prostym protoko³em który umo¿liwia wyszukiwanie iformacji
o u¿ytkownikach na innym serwerze, teraz ma ju¿ wspomaganie dla IPv6.
Pakiet ten zawiera klienta fingera. 

%package -n fingerd
Summary:	Finger server
Summary(pl):	Klient i serwer Finger 
Group:		Networking/Deamons
Group(pl):	Sieci/Serwery

%description -n fingerd
Finger is a simple protocol which allows users to find information about
users on other machines, now with IPv6 support. This package includes a 
standard finger server. The server runs from /etc/inetd.conf, 
which must be modified to disable finger requests.

%description -n fingerd -l pl
Finger jest prostym protoko³em który umo¿liwia wyszukiwanie iformacji
o u¿ytkownikach na innym serwerze, teraz ma ju¿ wspomaganie dla IPv6.
Pakiet ten zawiera serwer fingera. 

%package -n ping
Summary:	ping
Summary(pl):	ping
Group:		Networking
Group(pl):	Sieciowe

%description -n ping
ping

%description -n ping -l pl
ping

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
make CC="gcc $RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man{8,5},%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT{%{_libdir},/etc/ftp}

install -s ftp/ftp $RPM_BUILD_ROOT%{_bindir}

#touch $RPM_BUILD_ROOT/etc/ftp/nologin
touch $RPM_BUILD_ROOT/etc/ftp/welcome
touch $RPM_BUILD_ROOT/etc/ftp/motd
touch $RPM_BUILD_ROOT/etc/ftp/motd-6
touch $RPM_BUILD_ROOT/etc/ftp/users

install -s ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}
ln -sf ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd
install ftpd/ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/ftpd.8

#end ftp

#begin finger
install -s finger/finger $RPM_BUILD_ROOT%{_bindir}
install -s fingerd/fingerd $RPM_BUILD_ROOT%{_sbindir}
#end finger

#begin inet6-apps

install -s ping/ping $RPM_BUILD_ROOT%{_bindir}
install ping/ping.8 $RPM_BUILD_ROOT%{_mandir}/man8

install etc/hosts $RPM_BUILD_ROOT/etc
install man/hosts.5 $RPM_BUILD_ROOT%{_mandir}/man5

install -s lib/libinet6.a $RPM_BUILD_ROOT%{_libdir}
install -s misc/{gendata,socktest} $RPM_BUILD_ROOT%{_bindir}

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man?/*

%post -n ftpd
cat /etc/passwd | cut -d: -f1 | grep -v ftp >> \
	/etc/ftp/users

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*

%attr(0755,root,root) %{_bindir}/gendata
%attr(0755,root,root) %{_bindir}/socktest

%config(noreplace) %verify(not size mtime md5) /etc/hosts
%{_mandir}/man5/*

/usr/lib/*

%files -n ping
%defattr(644,root,root,755)
%attr(4711,root,root) %{_bindir}/ping
%{_mandir}/man8/ping*

%files -n ftpd
%defattr(644,root,root,755)
%dir /etc/ftp

%config(noreplace) %verify(not size mtime md5) /etc/ftp/welcome
%config(noreplace) %verify(not size mtime md5) /etc/ftp/motd
%config(noreplace) %verify(not size mtime md5) /etc/ftp/motd-6
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/ftp/users

%attr(755,root,root) %{_sbindir}/ftpd
%{_mandir}/man8/ftpd.*

%files -n ftp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ftp

%files -n finger
%attr(755,root,root) %{_bindir}/finger

%files -n fingerd
%attr(755,root,root) %{_sbindir}/fingerd

%changelog
* Tue May 25 1999 Artur Frysiak <wiget@pld.org.pl>
  [0.36-1]
- separate subpackages for servers
- separate subpackage for ping
- removed inetd6 (inetd has IPv6 support)
- removed tftp (please make another spec)
- removed /etc/ftp/nologin (ugly file)

* Mon Jan 18 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.35-2d]
- updated to latest version,
- changed permission of ping to 2711,
- compressed man pages.

* Fri Aug 14 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.33-3d]
- translation modified for pl,
- moved %changelog at the end of spec,
- changed permissions of all binaries to 711 and 4510 for ping,
- moved ftpconfig files from /etc to /etc/ftp.

* Sat Jul 11 1998 Marcin Korzonek <mkorz@shadow.eu.org>
  [0.33-2d]
- removed ftp client (won't work properly ;(

* Wed Jul 1 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.33-1d]
- first try at an RPM.
