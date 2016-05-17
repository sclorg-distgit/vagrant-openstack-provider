%{?scl:%scl_package %{vagrant_plugin_name}}
%{!?scl:%global pkg_name %{name}}

%global vagrant_plugin_name vagrant-openstack-provider

Summary: Enables Vagrant to manage machines in OpenStack Cloud
Name: %{?scl_prefix}%{vagrant_plugin_name}
Version: 0.7.2
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/ggiamarchi/vagrant-openstack-provider
Source0: http://rubygems.org/gems/%{vagrant_plugin_name}-%{version}.gem

Requires(posttrans): %{?scl_prefix}vagrant
Requires(preun): %{?scl_prefix}vagrant

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix}rubygem(colorize) = 0.7.3
Requires: %{?scl_prefix_ruby}rubygem(json)
Requires: %{?scl_prefix}rubygem(rest-client) >= 1.6.0
Requires: %{?scl_prefix}rubygem(rest-client) < 1.7.0
Requires: %{?scl_prefix}rubygem(sshkey) = 1.6.1
Requires: %{?scl_prefix}rubygem(terminal-table) = 1.4.5
Requires: %{?scl_prefix}vagrant

BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}vagrant
BuildArch: noarch
Provides: %{?scl_prefix}vagrant(%{vagrant_plugin_name}) = %{version}

%description
This is a Vagrant 1.6+ plugin that adds an OpenStack Cloud provider to Vagrant,
allowing Vagrant to control and provision machines within OpenStack cloud.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{vagrant_plugin_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{vagrant_plugin_name}.gemspec
%{?scl:EOF}

# remove specific version dep
sed -i '1,$s/<json>, \["= 1.8.3"]/<json>/g' %{vagrant_plugin_name}.gemspec

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{vagrant_plugin_name}.gemspec
%{?scl:EOF}
%vagrant_plugin_install

%install
mkdir -p %{buildroot}%{vagrant_plugin_dir}
cp -a .%{vagrant_plugin_dir}/* \
        %{buildroot}%{vagrant_plugin_dir}/

%posttrans
%{?scl:env -i - scl enable %{scl} - << \EOF}
%vagrant_plugin_register %{vagrant_plugin_name}
%{?scl:EOF}

%preun
%{?scl:env -i - scl enable %{scl} - << \EOF}
%vagrant_plugin_unregister %{vagrant_plugin_name}
%{?scl:EOF}

%files
%dir %{vagrant_plugin_instdir}
%{vagrant_plugin_libdir}
%{vagrant_plugin_instdir}/dummy.box
%{vagrant_plugin_instdir}/locales
%license %{vagrant_plugin_instdir}/LICENSE
%exclude %{vagrant_plugin_cache}
%{vagrant_plugin_spec}

%exclude %{vagrant_plugin_instdir}/.*
%exclude %{vagrant_plugin_instdir}/*.gemspec
%exclude %{vagrant_plugin_instdir}/functional_tests
%exclude %{vagrant_plugin_instdir}/Gemfile
%exclude %{vagrant_plugin_instdir}/Rakefile
%exclude %{vagrant_plugin_instdir}/Vagrantfile
%exclude %{vagrant_plugin_instdir}/spec
%exclude %{vagrant_plugin_instdir}/stackrc

%files doc
%doc %{vagrant_plugin_docdir}
%{vagrant_plugin_instdir}/example_box
%doc %{vagrant_plugin_instdir}/CHANGELOG.md
%doc %{vagrant_plugin_instdir}/RELEASE.md

%changelog
* Tue May 17 2016 Dominic Cleal <dominic@cleal.org> 0.7.2-1
- Initial build

