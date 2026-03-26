"use client";

import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo } from "react";

import { authStore, useAuthStore } from "@/src/store/authStore";

function getPageTitle(pathname: string): string {
	if (pathname.startsWith("/admin/eventos/") && pathname.split("/").length > 3) {
		return "Detalle de Evento";
	}

	if (pathname.startsWith("/admin/eventos")) {
		return "Eventos";
	}

	if (pathname.startsWith("/admin/personas")) {
		return "Usuarios y Asistentes";
	}

	if (pathname.startsWith("/admin")) {
		return "Panel de Administracion";
	}

	if (pathname.startsWith("/organizador/eventos/nuevo")) {
		return "Crear Evento";
	}

	if (pathname.startsWith("/organizador/eventos/") && pathname.endsWith("/editar")) {
		return "Editar Evento";
	}

	if (pathname.startsWith("/organizador/eventos/")) {
		return "Detalle de Evento";
	}

	if (pathname.startsWith("/organizador")) {
		return "Panel de Organizador";
	}

	return "Vinfinite Events";
}

function getRoleLabel(role?: string | null): string {
	if (role === "ADMIN") {
		return "ADMIN";
	}

	if (role === "ORGANIZADOR") {
		return "ORGANIZADOR";
	}

	return "INVITADO";
}

function getHomeRouteByRole(role?: string | null): string {
	if (role === "ADMIN") {
		return "/admin";
	}

	if (role === "ORGANIZADOR") {
		return "/organizador";
	}

	return "/";
}

interface AppChromeProps {
	children: React.ReactNode;
}

export function AppChrome({ children }: AppChromeProps) {
	const pathname = usePathname();
	const router = useRouter();
	const role = useAuthStore((state) => state.user?.role ?? null);

	useEffect(() => {
		void authStore.hydrate();
	}, []);

	const hideChrome = useMemo(() => {
		return pathname.startsWith("/login") || pathname.startsWith("/register");
	}, [pathname]);

	if (hideChrome) {
		return <>{children}</>;
	}

	const pageTitle = getPageTitle(pathname);
	const roleLabel = getRoleLabel(role);

	const handleGoHome = () => {
		router.push(getHomeRouteByRole(role));
	};

	return (
		<div className="relative isolate min-h-screen text-white">
			<div
				className="pointer-events-none fixed inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-80"
				style={{ backgroundImage: "url('/assets/images/fondo.jpeg')" }}
			/>

			<header className="sticky top-0 z-40 border-b border-white/20 bg-black/25 backdrop-blur-md">
				<div className="mx-auto flex w-full max-w-[1400px] items-center justify-between gap-2 px-3 py-3 sm:gap-4 sm:px-4 md:px-8">
					<button
						type="button"
						onClick={handleGoHome}
						className="flex min-w-0 flex-1 items-center gap-2 rounded-xl p-1 text-left transition-colors hover:bg-white/10 sm:gap-3"
						aria-label="Ir al inicio"
					>
						<Image src="/assets/logo/logo_vinfinite.png" alt="Vinfinite" width={48} height={48} className="h-10 w-10 rounded-lg sm:h-12 sm:w-12" />
						<div className="min-w-0">
							<p className="text-[10px] uppercase tracking-[0.14em] text-white/50 sm:text-xs sm:tracking-[0.2em]">VINFINITE</p>
							<h1 className="truncate text-base font-extrabold leading-tight sm:text-lg md:text-2xl">{pageTitle}</h1>
						</div>
					</button>
					<div className="shrink-0 rounded-full border border-[var(--color-secondary)]/40 bg-[var(--color-secondary)]/10 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.08em] text-[var(--color-secondary)] sm:px-3 sm:text-xs md:px-4 md:py-2">
						{roleLabel}
					</div>
				</div>
			</header>

			<main className="relative z-10">{children}</main>

			<footer className="relative z-10 border-t border-white/20 bg-black/25 px-4 py-6 backdrop-blur-md md:px-8">
				<div className="mx-auto grid w-full max-w-[1400px] grid-cols-1 gap-5 text-center text-sm text-white/80 md:grid-cols-3 md:text-left">
					<div>
						<p className="text-xs uppercase tracking-[0.14em] text-white/45">Contacto</p>
						<p className="mt-2">+503 78894537</p>
						<p>soporte@vinfinite.events</p>
					</div>
					<div>
						<p className="text-xs uppercase tracking-[0.14em] text-white/45">Redes</p>
						<div className="mt-2 flex items-center justify-center gap-2">
							<span className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-white/20">IG</span>
							<span className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-white/20">IN</span>
							<span className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-white/20">X</span>
						</div>
					</div>
					<div>
						<p className="text-xs uppercase tracking-[0.14em] text-white/45">Ubicacion</p>
						<p className="mt-2">Bulevar del Hipodromo, San Salvador, El Salvador</p>
					</div>
				</div>
				<div className="mx-auto mt-5 flex w-full max-w-[1400px] flex-wrap items-center justify-center gap-4 border-t border-white/10 pt-4 text-xs text-white/60">
					<button type="button" className="underline-offset-2 transition-colors hover:text-white hover:underline">
						Politicas de privacidad
					</button>
					<span className="hidden h-1 w-1 rounded-full bg-white/35 sm:inline-block" />
					<button type="button" className="underline-offset-2 transition-colors hover:text-white hover:underline">
						Terminos y condiciones
					</button>
				</div>
			</footer>
		</div>
	);
}
