Summary:        Software watchdog
Name:           watchdog
Version:        5.7
Release:        %mkrel 2
Group:          System/Kernel and hardware
License:        GPL & QPL
URL:            http://sourceforge.net/projects/watchdog/
Source0:        http://downloads.sourceforge.net/watchdog/%{name}-%{version}.tar.gz
Patch0:         watchdog-5.6-strfmt.patch
Requires(post): rpm-helper
Requires(postun): rpm-helper
Requires:       initscripts >= 4.97-49mdk
Requires:       kernel
BuildRequires:  kernel-headers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Watchdog monitors various aspects of a machine to ensure that is has not
locked up.  In the event that a machine has locked up, watchdog will envoke
a reboot of the system.

%prep
%setup -q
%patch0 -p1 -b .strfmt

%build
%configure2_5x
%make
mv README README.orig
iconv -f ISO-8859-1 -t UTF-8 < README.orig > README


%check
make check

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{_sysconfdir}
%makeinstall_std
install -Dp -m0644 redhat/sysconf.redhat %{buildroot}%{_sysconfdir}/sysconfig/watchdog
install -Dp -m0755 redhat/watchdog.init %{buildroot}%{_initrddir}/watchdog

%post
%_post_service watchdog

%preun
%_preun_service watchdog

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO README.watchdog.ipmi examples/
%attr(0755,root,root) %{_sbindir}/watchdog
%attr(0755,root,root) %{_sbindir}/wd_keepalive
%attr(0755,root,root) %{_initrddir}/watchdog
%{_mandir}/man5/watchdog.conf.5*
%{_mandir}/man8/watchdog.8*
%{_mandir}/man8/wd_keepalive.8*
%config(noreplace) %{_sysconfdir}/watchdog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/watchdog
