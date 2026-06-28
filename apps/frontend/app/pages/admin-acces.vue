<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-5xl">
      <div class="max-w-3xl">
        <h1 class="text-3xl font-semibold text-slate-950">Accès administrateur</h1>
        <p class="mt-3 text-slate-700">
          Demandez les droits nécessaires pour inviter des collaborateurs, attribuer les rôles et gérer les sources.
        </p>
      </div>

      <div class="mt-6 grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px]">
        <section class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
          <h2 class="text-lg font-semibold text-slate-950">Ce que couvre l’accès</h2>
          <ul class="mt-4 grid gap-3 text-sm text-slate-700 sm:grid-cols-2">
            <li class="rounded-md bg-slate-50 p-3 ring-1 ring-slate-200">Invitation collaborateurs</li>
            <li class="rounded-md bg-slate-50 p-3 ring-1 ring-slate-200">Gestion des rôles</li>
            <li class="rounded-md bg-slate-50 p-3 ring-1 ring-slate-200">MFA obligatoire à terme</li>
            <li class="rounded-md bg-slate-50 p-3 ring-1 ring-slate-200">Validation renforcée</li>
          </ul>
        </section>

        <aside class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
          <h2 class="text-lg font-semibold text-slate-950">Demande renforcée</h2>
          <p class="mt-3 text-sm leading-6 text-slate-700">
            Ce parcours prépare une demande. Il n’affiche aucun panneau administrateur fonctionnel tant que l’utilisateur et l’organisation ne sont pas validés.
          </p>
          <NuxtLink
            class="mt-5 inline-flex h-10 w-full items-center justify-center rounded-md bg-cyan-950 px-4 text-sm font-semibold text-white"
            to="/demande-acces?contexte=administrateur&role=admin"
          >
            Demander un accès administrateur
          </NuxtLink>
          <NuxtLink class="mt-3 inline-flex text-sm font-semibold text-slate-600 hover:text-slate-950" to="/connexion">Retour aux accès</NuxtLink>
        </aside>
      </div>

      <p class="mt-5 rounded-lg bg-indigo-50 p-4 text-sm text-indigo-950 ring-1 ring-indigo-100">
        Les privilèges ne sont activés qu’après validation de l’organisation et du responsable désigné.
      </p>
    </div>
  </section>
</template>
