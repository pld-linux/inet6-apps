Summary:	Inet6 Applications for Linux
Summary(pl):	Podstawowe aplikacje sieciowe ze wspomaganiem dla IPv6
Name:		inet6-apps
Version:	0.36
Release:	2
Copyright:	BSD & NRL
Source0:	ftp://ftp.inner.net/pub/ipv6/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-ftp.patch
Group:		Networking
Group(pl):	Sieciowe
Buildroot:	/tmp/%{name}-%{version}-root

%description
This is a kit of IPv6-aware applications designed to replace many of the
basic networking programs that come with your system. Most of these support
IPv4, IPv6, and UNIX domain sockets. 

%description -l pl
Pakiet ten zawiera podstawowe narz�dzia sieciowe wspieraj�ce nowy protok�
IPv6 i jest zamiennikiem starych aplikacji takich jak netkit-base.

%package -n	ftp6
Summary:	Standard Unix ftp (file transfer protocol) client
Summary(pl):	Standardowy klient ftp dla Linuxa
Group:		Networking
Group(pl):	Sieciowe
Requires:	%{name} = %{version}

%description -n ftp6
This provides the standard Unix command-line ftp client. Ftp 
is the standard Internet file transfer protocol, now with IPv6 support,
which is extremely popular for both file archives and file transfers 
between individuals.

%description -n ftp6 -l pl
Pakiet ten zawiera standardowego klienta ftp. Ftp 
(file transfer protocol) jest bardzo popularny w internecie i daje mo�liwo��
np.: �ci�gania oprogramowania z serwera na kt�rym klient nie ma konta.
Klient obecnie ma wspomaganie dla protoko�u IPv6

%package -n	ftpd6
Summary:	Standard Unix ftp (file transfer protocol) server
Summary(pl):	Standardowy serwer ftp dla Linuxa
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description -n ftpd6
This provides the standard Unix ftp server. Ftp 
is the standard Internet file transfer protocol, now with IPv6 support,
which is extremely popular for both file archives and file transfers 
between individuals.

%description -n ftpd6 -l pl
Pakiet ten zawiera standardowy server ftp. Ftp 
(file transfer protocol) jest bardzo popularny w internecie i daje mo�liwo��
np.: �ci�gania oprogramowania z serwera na kt�rym klient nie ma konta.
Serwer obecnie ma wspomaganie dla protoko�u IPv6

%package -n	finger6
Summary:	Finger client
Summary(pl):	Klient Finger 
Group:		Networking
Group(pl):	Sieciowe

%description -n finger6
Finger is a simple protocol which allows users to find information about
users on other machines, now with IPv6 support. This package includes a 
standard finger client. The server runs from /etc/inetd.conf, 
which must be modified to disable finger requests.

%description -n finger6 -l pl
Finger jest prostym protoko�em kt�ry umo�liwia wyszukiwanie iformacji
o u�ytkownikach na innym serwerze, teraz ma ju� wspomaganie dla IPv6.
Pakiet ten zawiera klienta fingera. 

%package -n	fingerd6
Summary:	Finger server
Summary(pl):	Klient i serwer Finger 
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery

%description -n fingerd6
Finger is a simple protocol which allows users to find information about
users on other machines, now with IPv6 support. This package includes a 
standard finger server. The server runs from /etc/inetd.conf, 
which must be modified to disable finger requests.

%description -n fingerd6 -l pl
Finger jest prostym protoko�em kt�ry umo�liwia wyszukiwanie iformacji
o u�ytkownikach na innym serwerze, teraz ma ju� wspomaganie dla IPv6.
Pakiet ten zawiera serwer fingera. 

%package -n	ping
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
%patch2 -p1
%patch3 -p1

%build
make CC="gcc $RPM_OPT_FLAGS" 
make -C ftpd YACC="bison -y" 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man{8,5},%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT/{bin,etc/ftpd}

install -s ftp/ftp $RPM_BUILD_ROOT%{_bindir}/ftp6

touch $RPM_BUILD_ROOT/etc/ftpd/welcome
touch $RPM_BUILD_ROOT/etc/ftpd/motd
touch $RPM_BUILD_ROOT/etc/ftpd/motd-6
touch $RPM_BUILD_ROOT/etc/ftpd/ftpusers

install -s ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd6
install ftpd/ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/ftpd.8

#end ftp

#begin finger
install -s finger/finger $RPM_BUILD_ROOT%{_bindir}/finger6
install -s fingerd/fingerd $RPM_BUILD_ROOT%{_sbindir}/fingerd6
#end finger

#begin inet6-apps

install -s ping/ping $RPM_BUILD_ROOT/bin
install ping/ping.8 $RPM_BUILD_ROOT%{_mandir}/man8

install etc/hosts $RPM_BUILD_ROOT/etc
install man/hosts.5 $RPM_BUILD_ROOT%{_mandir}/man5

install -s misc/{gendata,socktest} $RPM_BUILD_ROOT%{_bindir}

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man?/* doc/*

%post -n ftpd6
cat /etc/passwd | cut -d: -f1 | grep -v ftp >> \
	/etc/ftpd/ftpusers

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*

%attr(0755,root,root) %{_bindir}/gendata
%attr(0755,root,root) %{_bindir}/socktest

%config(noreplace) %verify(not size mtime md5) /etc/hosts
%{_mandir}/man5/*

%files -n ping
%defattr(644,root,root,755)
%attr(4711,root,root) /bin/ping
%{_mandir}/man8/ping*

%files -n ftpd6
%defattr(644,root,root,755)
%dir /etc/ftpd

%config(noreplace) %verify(not size mtime md5) /etc/ftpd/welcome
%config(noreplace) %verify(not size mtime md5) /etc/ftpd/motd
%config(noreplace) %verify(not size mtime md5) /etc/ftpd/motd-6
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/ftpd/ftpusers

%attr(755,root,root) %{_sbindir}/ftpd6

%{_mandir}/man8/ftpd*

%files -n ftp6
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ftp6

%files -n finger6
%attr(755,root,root) %{_bindir}/finger6

%files -n fingerd6
%attr(755,root,root) %{_sbindir}/fingerd6
