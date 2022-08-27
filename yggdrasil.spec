Name:           yggdrasil
Version:        0.4.4
Release:        1.im0%{?dist}
Summary:        End-to-end encrypted IPv6 networking

License:        GPLv3
URL:            https://yggdrasil-network.github.io
Source0:         https://codeload.github.com/yggdrasil-network/yggdrasil-go/tar.gz/v%{version}

# $ GOPROXY=https://proxy.golang.org go mod vendor -v
# Contains yggdrasil-go-%{version}/vendor/*.
Source1:    %{name}-go-%{version}.go-mod-vendor.tar.xz

Patch0:     0001-Restart-without-limits.patch

%{?systemd_requires}
BuildRequires:  systemd golang >= 1.17 git
Requires(pre):  shadow-utils
Conflicts:      yggdrasil-develop

%description
Yggdrasil is a proof-of-concept to explore a wholly different approach to
network routing. Whereas current computer networks depend heavily on very
centralised design and configuration, Yggdrasil breaks this mould by making
use of a global spanning tree to form a scalable IPv6 encrypted mesh network.

%define debug_package %{nil}

%pre
getent group yggdrasil >/dev/null || groupadd -r yggdrasil
exit 0

%prep
%autosetup -p1 -b0 -n %{name}-go-%{version}
%autosetup -p1 -b1 -n %{name}-go-%{version}

%build
export PKGNAME="%{name}"
export PKGVER="%{version}"
./build -t -p -l "-linkmode=external"

%install
rm -rf %{buildroot}
install -m 0755 -D yggdrasil %{buildroot}/%{_bindir}/yggdrasil
install -m 0755 -D yggdrasilctl %{buildroot}/%{_bindir}/yggdrasilctl
install -m 0755 -D contrib/systemd/yggdrasil-default-config.service %{buildroot}/%{_sysconfdir}/systemd/system/yggdrasil-default-config.service
install -m 0755 -D contrib/systemd/yggdrasil.service %{buildroot}/%{_sysconfdir}/systemd/system/yggdrasil.service

%files
%{_bindir}/yggdrasil
%{_bindir}/yggdrasilctl
%{_sysconfdir}/systemd/system/yggdrasil-default-config.service
%{_sysconfdir}/systemd/system/yggdrasil.service

%post
%systemd_post yggdrasil-default-config.service
%systemd_post yggdrasil.service

%preun
%systemd_preun yggdrasil-default-config.service
%systemd_preun yggdrasil.service

%postun
%systemd_postun_with_restart yggdrasil-default-config.service
%systemd_postun_with_restart yggdrasil.service
