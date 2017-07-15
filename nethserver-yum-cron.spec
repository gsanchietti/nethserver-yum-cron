Summary: nethserver - configure yum-cron
%define name nethserver-yum-cron
Name: %{name}
%define version 0.0.5
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: yum-cron
Requires: perl-Email-Valid
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
configure yum-cron for automatic update

%changelog
* Sat Jul 15 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.5-1.ns6
- Sanitise the custom yum exclusion
- code from dnutan

* Wed Jul 12 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.4-1.ns6
- Sanitise the custom yum exclusion

* Sat Jul 08 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.3-1.ns6
- Added YumCron_Description
- you can define when the job starts by randomWait

* Fri Jun 23 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.2-1.ns6
- initial

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
/sbin/chkconfig yum-cron on

%postun
/sbin/chkconfig yum-cron off
/sbin/service yum-cron stop

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING
