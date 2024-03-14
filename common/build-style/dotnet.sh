#
# This helper is for building dotnet projects
#

do_build() {
	: ${make_cmd:=dotnet}

	local _runtime="${XBPS_DOTNET_TARGET}"
	if [ "$CROSS_BUILD" ]; then
		_runtime="${XBPS_CROSS_DOTNET_TARGET}"
	fi

	${make_cmd} publish \
		--no-self-contained "True" \
		--configuration "Release" \
		--runtime "${_runtime}" \
		--nologo "True" \
		--output "_publish" \
		${configure_args} ${make_build_args}
}

do_check() {
	: ${make_cmd:=dotnet}

	local _runtime="${XBPS_DOTNET_TARGET}"
	if [ "$CROSS_BUILD" ]; then
		_runtime="${XBPS_CROSS_DOTNET_TARGET}"
	fi

	${make_check_pre} ${make_cmd} test \
		--configuration "Release" \
		--runtime "${_runtime}" \
		--nologo "True" \
		--no-restore "True" \
		${configure_args} ${make_check_args}
}

do_install() {
	cp -a "_publish" "$DESTDIR/usr/lib/$pkgname"
}
