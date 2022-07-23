Summary:        Software watchdog
Name:           watchdog
Version:        5.16
Release:        1
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

%description
Watchdog monitors various aspects of a machine to ensure that is has not
locked up.  In the event that a machine has locked up, watchdog will envoke
a reboot of the system.

%prep
%setup -q
#%patch0 -p1 -b .strfmt

%build
%configure2_5x
%make
mv README README.orig
iconv -f ISO-8859-1 -t UTF-8 < README.orig > README


%check
make check

%install
install -d -m0755 %{buildroot}%{_sysconfdir}
%makeinstall_std
install -Dp -m0644 redhat/sysconf.redhat %{buildroot}%{_sysconfdir}/sysconfig/watchdog
install -Dp -m0755 redhat/watchdog.init %{buildroot}%{_initrddir}/watchdog

%post
%_post_service watchdog

%preun
%_preun_service watchdog

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO README.watchdog.ipmi examples/
%attr(0755,root,root) %{_sbindir}/watchdog
%attr(0755,root,root) %{_sbindir}/wd_keepalive
%attr(0755,root,root) %{_sbindir}/wd_identify
%attr(0755,root,root) %{_initrddir}/watchdog
%{_mandir}/man5/watchdog.conf.5*
%{_mandir}/man8/watchdog.8*
%{_mandir}/man8/wd_identify.8*
%{_mandir}/man8/wd_keepalive.8*
%config(noreplace) %{_sysconfdir}/watchdog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/watchdog


%changelog
* Fri Jun 15 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.12-1
+ Revision: 805794
- version update 5.12

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 5.7-2mdv2011.0
+ Revision: 615432
- the mass rebuild of 2010.1 packages

* Wed Jan 06 2010 Frederik Himpe <fhimpe@mandriva.org> 5.7-1mdv2010.1
+ Revision: 486793
- update to new version 5.7

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 5.6-2mdv2010.0
+ Revision: 445737
- rebuild

* Sun Mar 22 2009 Frederik Himpe <fhimpe@mandriva.org> 5.6-1mdv2009.1
+ Revision: 360398
- Update to new version 5.6
- Remove unneeded patches and hacks
- Add patch fixing build with -Werror=format-security

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 5.4-2mdv2009.0
+ Revision: 239010
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 17 2007 David Walluck <walluck@mandriva.org> 5.4-1mdv2008.0
+ Revision: 65319
- 5.4
- add udev support
- rediff initscript patch

* Wed Jun 20 2007 David Walluck <walluck@mandriva.org> 5.3.1-1mdv2008.0
+ Revision: 41716
- spec cleanup
- fix PreReq use
- 5.3.1
- use pristine source
- remove unneeded patches
- own /dev/watchdog
- create /dev/watchdog before service start
- more explicit file list
- LSB init support

