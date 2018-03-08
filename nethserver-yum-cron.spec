Summary: nethserver - configure yum-cron
Name: nethserver-yum-cron
Version: 0.1.7
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: yum-cron
Requires: perl-Email-Valid

BuildRequires: nethserver-devtools

%description
configure yum-cron for automatic update

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf %{buildroot}
(cd root   ; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} \
> %{name}-%{version}-%{release}-filelist

%clean 
rm -rf %{buildroot}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING

%changelog
* Sat Jul 08 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.1.7-1.ns7
- Added YumCron_Description
- you can define when the job starts by randomWait

* Fri Jun 23 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 0.1.6-1.ns7
- initial

