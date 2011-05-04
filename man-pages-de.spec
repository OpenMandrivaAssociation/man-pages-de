%define LNG de

Summary: German man (manual) pages from the Linux Documentation Project
Name: man-pages-%LNG
Version: 0.5
Release: %mkrel 9
License: Distributable
Group: System/Internationalization
Source: http://www.infodrom.org/projects/manpages-de/download/manpages-de-%{version}.tar.bz2  
Patch1: man-pages-de-0.3-nolocalfile.patch
URL: http://www.infodrom.org/projects/manpages-de/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LNG, man => 1.5j-8mdk
BuildArch: noarch
Obsoletes: man-%LNG, manpages-%LNG
Provides: man-%LNG, manpages-%LNG

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
%setup -q -n manpages-de-%{version}
%patch1 -p1

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/%LNG/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}/var/catman/%LNG/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 3 4 5 6 7 8; do
	cp -adpvrf man$i %{buildroot}/%_mandir/%LNG/
done

# those files conflict whith net-tools
rm %{buildroot}/%_mandir/de/man1/hostname.1

LANG=%LNG DESTDIR=%{buildroot} %{_sbindir}/makewhatis %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_sbindir}/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       rm -rf /var/catman/%LNG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man, 0755)
%doc CHANGES README COPYRIGHT
%defattr(0644,root,man, 755)
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%_mandir/%LNG/whatis
%attr(755,root,man) /var/catman/%LNG
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
