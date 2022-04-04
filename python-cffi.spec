#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	doc	# Sphinx based documentation
%bcond_without	tests	# unit tests
#
Summary:	Foreign Function Interface for Python 2 calling C code
Summary(pl.UTF-8):	Interfejs funkcji obcych (FFI) dla Pythona 2 wywołującego kod w C
Name:		python-cffi
Version:	1.15.0
Release:	4
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cffi/
Source0:	https://files.pythonhosted.org/packages/source/c/cffi/cffi-%{version}.tar.gz
# Source0-md5:	f3a3f26cd3335fc597479c9475da0a0b
URL:		http://cffi.readthedocs.org/
BuildRequires:	libffi-devel >= 3
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python >= 1:2.6
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pycparser
BuildRequires:	python-pytest
BuildRequires:	virtualenv
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pycparser
BuildRequires:	python3-pytest
BuildRequires:	virtualenv
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python-modules >= 1:2.6
Requires:	python-pycparser
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Foreign Function Interface for Python calling C code. The aim of this
project is to provide a convenient and reliable way of calling C code
from Python without learning additional language or API.

This package contains Python 2 module.

%description -l pl.UTF-8
CFFI to interfejs funkcji obcych (FFI - foreign Function Interface) do
wywoływania kodu w C z Pythona. Celem projektu jest dostarczenie
wygodnego i wiarygodnego sposobu wywoływania kodu w C z Pythona bez
potrzeby nauki dodatkowego języka lub API.

Ten pakiet zawiera moduł Pythona 2.

%package -n python3-cffi
Summary:	Foreign Function Interface for Python 3 calling C code
Summary(pl.UTF-8):	Interfejs funkcji obcych (FFI) dla Pythona 3 wywołującego kod w C
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2
Requires:	python3-pycparser

%description -n python3-cffi
Foreign Function Interface for Python calling C code. The aim of this
project is to provide a convenient and reliable way of calling C code
from Python without learning additional language or API.

This package contains Python 3 module.

%description -n python3-cffi -l pl.UTF-8
CFFI to interfejs funkcji obcych (FFI - foreign Function Interface) do
wywoływania kodu w C z Pythona. Celem projektu jest dostarczenie
wygodnego i wiarygodnego sposobu wywoływania kodu w C z Pythona bez
potrzeby nauki dodatkowego języka lub API.

Ten pakiet zawiera moduł Pythona 3.

%package apidocs
Summary:	API documentation for Python CFFI module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona CFFI
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python CFFI module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona CFFI.

%prep
%setup -q -n cffi-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd):$(echo $(pwd)/build-2/lib.linux-*) \
%{__python} -m pytest c testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd):$(echo $(pwd)/build-3/lib.linux-*) \
%{__python3} -m pytest c testing
%endif
%endif

%if %{with doc}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{py_sitedir}/_cffi_backend.so
%dir %{py_sitedir}/cffi
%{py_sitedir}/cffi/_cffi_errors.h
%{py_sitedir}/cffi/_cffi_include.h
%{py_sitedir}/cffi/_embedding.h
%{py_sitedir}/cffi/parse_c_type.h
%{py_sitedir}/cffi/*.py[co]
%{py_sitedir}/cffi-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-cffi
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{py3_sitedir}/_cffi_backend.cpython-*.so
%dir %{py3_sitedir}/cffi
%{py3_sitedir}/cffi/_cffi_errors.h
%{py3_sitedir}/cffi/_cffi_include.h
%{py3_sitedir}/cffi/_embedding.h
%{py3_sitedir}/cffi/parse_c_type.h
%{py3_sitedir}/cffi/*.py
%{py3_sitedir}/cffi/__pycache__
%{py3_sitedir}/cffi-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,*.html,*.js}
%endif
