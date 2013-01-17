%define	LNG de
%define	gitrevision aeb3e35
%define	srcname manpages-%{LNG}

Name:		man-pages-%{LNG}
Version:	0.9
Release:	2
Summary:	German man (manual) pages from the Linux Documentation Project
License:	Distributable
Group:		System/Internationalization
Url:		http://alioth.debian.org/projects/manpages-de/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Source0:	%{srcname}-%{gitrevision}.tar.gz
BuildRequires:	man
Requires:	locales-%{LNG}
Requires:	man
Obsoletes:	man-%{LNG}
Obsoletes:	manpages-%{LNG}
Provides:	man-%{LNG}
Provides:	manpages-%{LNG}

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to German.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd,
                    nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)

%prep
%setup -q -n %{srcname}-%{gitrevision}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_mandir}/%{LNG}/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}%{_var}/catman/%{LNG}/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 3 4 5 6 7 8; do
	if [ -d man$i ] ; then
		cp -avf man$i %{buildroot}%{_mandir}/%{LNG}/
	else
		echo "man$i does not exist"
	fi
done

# those files conflict whith net-tools
# nothing to remove for now

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%{_mandir}/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}%{_var}/cache/man/%{LNG}

touch %{buildroot}%{_var}/cache/man/%{LNG}/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%{LNG}, if there isn't any man page
   ## directory /%{_mandir}/%{LNG}
   if [ ! -d %{_mandir}/%{LNG} ] ; then
       rm -rf %{_var}/catman/%{LNG}
   fi
fi

%post
%create_ghostfile %{_var}/cache/man/%{LNG}/whatis root root 644

%files
%doc CHANGES README COPYRIGHT
%dir %{_mandir}/%{LNG}
%dir %{_var}/cache/man/%{LNG}
%ghost %config(noreplace) %{_var}/cache/man/%{LNG}/whatis
%{_mandir}/%{LNG}/man*
#%{_mandir}/%{LNG}/whatis
%attr(755,root,man) %{_var}/catman/%{LNG}
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron



%changelog
* Wed Dec 14 2011 Andrey Bondrov <abondrov@mandriva.org> 0.9-1mdv2012.0
+ Revision: 741152
- New version 0.9 from git, new upstream url

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5-9
+ Revision: 666367
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-8mdv2011.0
+ Revision: 609318
- rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-7mdv2011.0
+ Revision: 609300
- fix build
- fix typos
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.5-5mdv2009.1
+ Revision: 351569
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.5-4mdv2009.0
+ Revision: 223171
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.5-3mdv2008.1
+ Revision: 152929
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.5-2mdv2008.1
+ Revision: 152924
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Apr 24 2007 Thierry Vignaud <tv@mandriva.org> 0.5-1mdv2008.0
+ Revision: 17838
- new release


* Thu Mar 02 2006 Götz Waschk <waschk@mandriva.org> 0.4-5mdk
- drop patch 0
- drop prereq
- drop icon
- fix URL

* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.4-4mdk
- rebuild

