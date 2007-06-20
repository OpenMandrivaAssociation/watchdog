Name:           watchdog
Version:        5.3.1
Release:        %mkrel 1
Summary:        Software watchdog
Group:          System/Kernel and hardware
License:        GPL & QPL
URL:            http://metalab.unc.edu/pub/Linux/system/daemons/watchdog/
Source0:        ftp://metalab.unc.edu/pub/Linux/system/daemons/watchdog/watchdog_%{version}.tar.gz
Patch0:         watchdog-5.2.3.patch
Patch1:         watchdog-5.2.3-x86_64.patch
Requires(post): rpm-helper
Requires(postun): rpm-helper
Requires:       common-licenses
Requires:       initscripts >= 4.97-49mdk
Requires:       kernel
BuildRequires:  kernel-headers
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Watchdog monitors various aspects of a machine to ensure that is has not
locked up.  In the event that a machine has locked up, watchdog will envoke
a reboot of the system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{configure2_5x}
%{make}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man{5,8}
install -m644 watchdog.conf %{buildroot}%{_sysconfdir}/
install -m644 watchdog.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/watchdog
install -m755 rc.watchdog.redhat %{buildroot}%{_initrddir}/watchdog 
install -m755 src/watchdog %{buildroot}%{_sbindir}/
install -m644 watchdog.8 %{buildroot}%{_mandir}/man8/
install -m644 watchdog.conf.5 %{buildroot}%{_mandir}/man5/

%{__mkdir_p} %{buildroot}/dev
/bin/touch %{buildroot}/dev/watchdog

%check
%{make} check

%clean
rm -rf %{buildroot}

%post
[ ! -c /dev/watchdog ] && /bin/mknod /dev/watchdog c 10 130 || :
%_post_service watchdog

%preun
%_preun_service watchdog

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%attr(0755,root,root) %{_sbindir}/watchdog
%attr(0755,root,root) %{_initrddir}/watchdog
%{_mandir}/man5/watchdog.conf.5*
%{_mandir}/man8/watchdog.8*
%config(noreplace) %{_sysconfdir}/watchdog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/watchdog
%ghost /dev/watchdog
