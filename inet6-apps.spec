Summary:     Inet6 Applications for Linux
Name:        inet6-apps
Version:     0.36
Release:     1
Copyright:   BSD & NRL
Source:      ftp://ftp.inner.net/pub/ipv6/%{name}-%{version}.tar.gz
Source1:     ftp://ftp.inner.net/pub/ipv6/tftpd-1.2a1.tar.gz
Patch:       %{name}-config.patch
Patch1:	     %{name}-paths.patch
Patch2:      tftpd.patch
Patch3:	     %{name}-ipv6.patch
Group:       Networking
Group(pl):   Sieci
BuildRoot:	/tmp/%{name}-%{version}-root
Summary(pl): Podstawowe aplikacje sieciowe ze wspomaganiem dla IPv6

%description
This is a kit of IPv6-aware applications designed to replace many of the
basic networking programs that come with your system. Most of these support
IPv4, IPv6, and UNIX domain sockets. 

%description -l pl
Pakiet ten zawiera podstawowe narzêdzia sieciowe wspieraj±ce nowy protokó³
IPv6 i jest zamiennikiem starych aplikacji takich jak netkit-base.

%package -n ftp
Summary:     Standard Unix ftp (file transfer protocol) client and server
Group:       Networking
Group(pl):   Sieci
Requires:    %{name} = %{version}
Summary(pl): Standardowy klient i serwer ftp dla Linuxa

%description -n ftp
This provides the standard Unix command-line ftp client and server. Ftp 
is the standard Internet file transfer protocol, now with IPv6 support,
which is extremely popular for both file archives and file transfers 
between individuals.

%description -n ftp -l pl
Pakiet ten zawiera standardowego klienta i servera ftp. Ftp 
(file transfer protocol) jest bardzo popularny w internecie i daje mo¿liwo¶æ
np.: ¶ci±gania oprogramowania z serwera na którym klient nie ma konta.
Klient i serwer obecnie maj± wspomaganie dla protoko³u IPv6

%package -n finger
Summary:     Finger client and server
Group:       Networking
Group(pl):   Sieci
Summary(pl): Klient i serwer Finger 

%description -n finger
Finger is a simple protocol which allows users to find information about
users on other machines, now with IPv6 support. This package includes a 
standard finger client and server. The server runs from /etc/inetd.conf, 
which must be modified to disable finger requests.

%description -n finger -l pl
Finger jest prostym protoko³em który umo¿liwia wyszukiwanie iformacji
o u¿ytkownikach na innym serwerze, teraz ma ju¿ wspomaganie dla IPv6.
Pakiet ten zawiera klienta i serwer fingera. 

%package -n tftp
Summary:     Client and daemon for the trivial file transfer protocol (tftp)
Group:       Networking
Group(pl):   Sieci
Summary(pl): Klient i demon tftp (trivial file transfer protocol)

%description -n tftp
The trivial file transfer protocol (tftp) is normally used only for 
booting diskless workstations, now with IPv6 support. It provides very 
little security, and should not be enabled unless it is needed. The 
tftp server is run from /etc/inetd.conf.

%description -n tftp -l pl
Tftp (trivial file transfer protocol) jest u¿ywany g³ównie do startowania
stacji bezdyskowych z sieci, obecnie ma wspomaganie dla IPv6. Demon
powinien byæ uruchamiany tylko wtedy, kiedy zachodzi taka konieczno¶æ. 

%prep
%setup -q
%setup  -q -D -T -a 1
%patch  -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make CC="gcc $RPM_OPT_FLAGS" 
(cd tftpd-1.2a1; ./configure --prefix=/usr; make CCOPT="$RPM_OPT_FLAGS") 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man{8,5}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT/etc/ftp

install -s ftp/ftp $RPM_BUILD_ROOT%{_bindir}

touch $RPM_BUILD_ROOT/etc/ftp/nologin
touch $RPM_BUILD_ROOT/etc/ftp/welcome
touch $RPM_BUILD_ROOT/etc/ftp/motd
touch $RPM_BUILD_ROOT/etc/ftp/motd-6
touch $RPM_BUILD_ROOT/etc/ftp/users

install -s ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}
ln -sf ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd6
install ftpd/ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/ftpd6.8

#end ftp

#begin tftp

install -s tftpd-1.2a1/tftpd $RPM_BUILD_ROOT%{_sbindir}
install -s tftp/tftp $RPM_BUILD_ROOT%{_bindir}
#end tftp

#begin finger
install -s finger/finger $RPM_BUILD_ROOT%{_bindir}
install -s fingerd/fingerd $RPM_BUILD_ROOT%{_sbindir}
#end finger

#begin inet6-apps

install -s ping/ping $RPM_BUILD_ROOT%{_bindir}
install ping/ping.8 $RPM_BUILD_ROOT%{_mandir}/man8

install etc/hosts $RPM_BUILD_ROOT/etc
install man/hosts.5 $RPM_BUILD_ROOT%{_mandir}/man5
install -s inetd/inetd $RPM_BUILD_ROOT%{_sbindir}/inetd6

install lib/libinet6.a $RPM_BUILD_ROOT%{_libdir}
install -s misc/gendata $RPM_BUILD_ROOT%{_bindir}
install -s misc/socktest $RPM_BUILD_ROOT%{_bindir}

#cat GNUmakefile.inc | sed s:"DOTS=../":"DOTS=/usr/lib/":g > \
#    $RPM_BUILD_ROOT%{_libdir}/GNUmakefile.inc

bzip2 -9 $RPM_BUILD_ROOT%{_mandir}/{man5/*,man8/*}

%post -n ftp
cat /etc/passwd | sed s/:/" "/g | awk '{ print $1 }' | grep -v ftp >> \
/etc/ftp/users

%files
%defattr(644,root,root,755)
%doc doc/*

%attr(0711,root,root) %{_bindir}/gendata
%attr(0711,root,root) %{_bindir}/socktest
%attr(0711,root,root) %{_sbindir}/inetd6
%attr(2711,root,icmp) %{_bindir}/ping

%config(noreplace) %verify(not size mtime md5) /etc/hosts

/usr/lib/*

%attr(644,root,man) %{_mandir}/man5/*
%attr(644,root,man) %{_mandir}/man8/ping*

%files -n ftp
%defattr(644,root,root,755)
%dir /etc/ftp

%attr(600,root,root) %config %verify(not size mtime md5) /etc/ftp/nologin
%attr(644,root,root) %config %verify(not size mtime md5) /etc/ftp/welcome
%attr(644,root,root) %config %verify(not size mtime md5) /etc/ftp/motd
%attr(644,root,root) %config %verify(not size mtime md5) /etc/ftp/motd-6
%attr(600,root,root) %config %verify(not size mtime md5) /etc/ftp/users

%attr(711,root,root) %{_bindir}/ftp
%attr(711,root,root) %{_sbindir}/ftpd6
%attr(711,root,root) %{_sbindir}/ftpd
%attr(644,root, man) %{_mandir}/man8/ftpd6.*

%files -n finger
%attr(711,root,root) %{_bindir}/finger
%attr(711,root,root) %{_sbindir}/fingerd

%files -n tftp
%attr(711,root,root) %{_bindir}/tftp
%attr(711,root,root) %{_sbindir}/tftpd

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
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
