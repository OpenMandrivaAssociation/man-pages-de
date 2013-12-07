%define	LNG de
%define	gitrevision aeb3e35
%define	srcname manpages-%{LNG}

Summary:	German man (manual) pages from the Linux Documentation Project
Name:		man-pages-%{LNG}
Version:	0.9
Release:	6
License:	Distributable
Group:		System/Internationalization
Url:		http://alioth.debian.org/projects/manpages-de/
Source0:	%{srcname}-%{gitrevision}.tar.gz
BuildArch:	noarch
BuildRequires:	man
Requires:	locales-%{LNG}
Requires:	man

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
%setup -qn %{srcname}-%{gitrevision}

%build

%install
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
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
%attr(755,root,man) %{_var}/catman/%{LNG}
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

