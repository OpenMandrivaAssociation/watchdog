%define name watchdog
%define version 5.2.3
%define release 2mdk

Summary: Software watchdog
Name: %{name}
Version: %{version}
Release: %release
Group: System/Kernel and hardware
License: GPL & QPL
URL: http://metalab.unc.edu/pub/Linux/system/daemons/watchdog/
Source0: ftp://metalab.unc.edu/pub/Linux/system/daemons/watchdog/%{name}-%{version}.tar.bz2
Patch0: watchdog-5.2.3.patch
Patch1: watchdog.sundries.patch
Patch2: watchdog-5.2.3-errno.patch
Patch3: watchdog-5.2.3-x86_64.patch
PreReq: rpm-helper
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: kernel-headers
Requires: initscripts >= 4.97-49mdk kernel common-licenses

%description
Watchdog monitors various aspects of a machine to ensure that is has not
locked up.  In the event that a machine has locked up, watchdog will envoke
a reboot of the system.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .mdk
%patch1 -p1 -b .sundries
%patch2 -p1 -b .errno
%patch3 -p1 -b .x86_64

%build
%configure2_5x
%make

%install
rm -fr %{buildroot}
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

%post
%_post_service watchdog
[ ! -c /dev/watchdog ] && mknod /dev/watchdog c 10 130
exit 0

%preun
%_preun_service watchdog

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%config(noreplace) %{_sysconfdir}/watchdog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/watchdog
%{_initrddir}/watchdog
%{_sbindir}/watchdog
%{_mandir}/*/*

%changeLog
* Tue May 10 2005 Frederic Lepied <flepied@mandriva.com> 5.2.3-2mdk
- fix build on x86_64

* Tue Jun  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 5.2.3-1mdk
- 5.2.3
- open /dev/watchdog by default

* Thu Jun 27 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.2-2mdk
- patch1: patch sundries.cc

* Fri Sep 14 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.2-1mdk
- added by Oden Eriksson <oden.eriksson@kvikkjokk.net> :
	- initial cooker contrib
	- update to 5.2
	- added patch0

* Sat Jun 24 2000 Soenke J. Peters <peters+rpm@simprovement.com>
- RedHat Build

* Wed Apr 19 2000 Marc Christensen <marc@calderasystems.com>
- Initial Caldera Build
