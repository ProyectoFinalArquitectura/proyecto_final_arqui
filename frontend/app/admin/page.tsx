"use client";

import { useRouter } from "next/navigation";

import { authStore } from "@/src/store/authStore";

export default function AdminPage() {
  const router = useRouter();

  const handleLogout = () => {
    authStore.logout();
    router.push("/login");
  };

  return (
    <main className="min-h-screen px-6 py-10 text-white">
      <div className="glass-bar mx-auto max-w-3xl rounded-3xl p-8 transition-all duration-300">
        <p className="text-sm uppercase tracking-[0.24em] text-white/55">Administrador</p>
        <h1 className="mt-3 text-3xl font-extrabold">Panel admin en construccion</h1>
        <p className="mt-3 text-white/70">
          Login exitoso. Esta vista confirma que la redireccion por rol ADMIN esta funcionando.
        </p>
        <button
          className="focus-outline mt-8 rounded-2xl bg-[var(--color-secondary)] px-5 py-3 text-sm font-bold text-black"
          onClick={handleLogout}
          type="button"
        >
          Cerrar sesion
        </button>
      </div>
    </main>
  );
}
