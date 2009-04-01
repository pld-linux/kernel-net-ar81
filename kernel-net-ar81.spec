#
# TODO:
#		- remove from cvs when 2.6.27@kernel.spec will be ready.
#		http://git.kernel.org/?p=linux/kernel/git/torvalds/linux-2.6.git;a=commit;h=a6a5325239c20202e18e21e94291bccc659fbf9e
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		rel	2
Summary:	Linux driver for the Atheros AR8121/8131 PCI-E cards
Name:		kernel%{_alt_kernel}-net-ar81
Version:	1.0.1.0
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	AR81Family-linux-v%{version}.tar.gz
# Source0-md5:	e9559d2ae25be6db327c7ec40e922438
Patch0:		kernel-net-ar81-2.6.29.patch
URL:		http://www.unav-micro.com/Drivers.aspx
BuildRequires:	dos2unix
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(atl1e) = %{version}-%{rel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for the Atheros AR8121/8131 cards.

This package contains Linux module.

%prep
%setup -q -c %{name}
find . -type f | xargs dos2unix
%patch0 -p1

%build
cat > src/Makefile << 'EOF'
CFILES = at_main.c at_hw.c at_param.c at_ethtool.c kcompat.c
obj-m += atl1e.o
atl1e-objs := $(CFILES:.c=.o)
EXTRA_CFLAGS += -DDBG=0
EOF

%build_kernel_modules -C src -m atl1e

%install
rm -rf $RPM_BUILD_ROOT
install atl1e.7 -D $RPM_BUILD_ROOT%{_mandir}/man7/atl1e.7

%install_kernel_modules -m src/atl1e -d kernel/drivers/net

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc readme release_note.txt
/lib/modules/%{_kernel_ver}/kernel/drivers/net/atl1e.ko*
%{_mandir}/man7/*
