Name:           watchdog
Version:        5.4
Release:        %mkrel 1
Summary:        Software watchdog
Group:          System/Kernel and hardware
License:        GPL & QPL
URL:            http://metalab.unc.edu/pub/Linux/system/daemons/watchdog/
Source0:        ftp://metalab.unc.edu/pub/Linux/system/daemons/watchdog/watchdog-%{version}.tar.gz
Source1:        watchdog-udev.nodes
Source2:        watchdog-makedev.d-watchdog
Source3:        watchdog-udev.rules
Patch0:         watchdog-5.4-init.patch
Patch1:         watchdog-5.2.3-x86_64.patch
Requires(post): rpm-helper
Requires(postun): rpm-helper
Requires:       common-licenses
Requires:       initscripts >= 4.97-49mdk
Requires:       kernel
BuildRequires:  kernel-headers

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
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__mkdir_p} %{buildroot}%{_mandir}/man{5,8}
%{__cp} -a watchdog.conf %{buildroot}%{_sysconfdir}/
%{__cp} -a watchdog.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/watchdog
%{__cp} -a rc.watchdog.redhat %{buildroot}%{_initrddir}/watchdog 
%{__cp} -a src/watchdog %{buildroot}%{_sbindir}/
%{__cp} -a watchdog.8 %{buildroot}%{_mandir}/man8/
%{__cp} -a watchdog.conf.5 %{buildroot}%{_mandir}/man5/

%{__mkdir_p} %{buildroot}%{_sysconfdir}/udev/devices.d
%{__cp} -a %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/devices.d/99-watchdog.nodes
%{__mkdir_p} %{buildroot}%{_sysconfdir}/makedev.d
%{__cp} -a %{SOURCE2} %{buildroot}%{_sysconfdir}/makedev.d/z-watchdog
%{__mkdir_p} %{buildroot}%{_sysconfdir}/udev/rules.d/
%{__cp} -a %{SOURCE3} %{buildroot}%{_sysconfdir}/udev/rules.d/99-watchdog.rules

%check
%{make} check

%clean
%{__rm} -rf %{buildroot}

%post
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
%config(noreplace) %{_sysconfdir}/makedev.d/z-watchdog
%config(noreplace) %{_sysconfdir}/udev/rules.d/99-watchdog.rules
%config(noreplace) %{_sysconfdir}/udev/devices.d/99-watchdog.nodes

