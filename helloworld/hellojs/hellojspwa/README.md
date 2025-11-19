# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.

# how to run with ssl
make keys e.g. for localhost:
https://hackernoon.com/how-to-get-sslhttps-for-localhost-i11s3342

```bash
npm run build
node server.js
```

also generate svelte pwa app with:  npm create @vite-pwa/pwa@latest
Debugger attached.
Need to install the following packages:
@vite-pwa/create-pwa@0.5.0
Ok to proceed? (y) y


> npx
> create-pwa

Debugger attached.
✔ Project name: … vite-project
✔ Select a framework: › Svelte
✔ Select a variant: › SvelteKit ↗
✔ PWA Name: … hellojspwa
✔ PWA Short Name: … hellojspwa
✔ PWA Description: … 
✔ Theme color: … #ffffff
✔ Select a strategy: › generateSW
✔ Select a behavior: › Auto update
✔ Enable periodic SW updates? … no / yes
✔ Show offline ready prompt? … no / yes
✔ Generate PWA Assets Icons on the fly? … no / yes
Debugger attached.
Need to install the following packages:
sv@0.6.6
Ok to proceed? (y) 

also try https://svelte.dev/docs/kit/service-workers#Inside-the-service-worker
https://stackoverflow.com/questions/77647463/sveltekit-webapp-to-pwa-progressive-web-app-how-to-do-it-in-the-most-simple-w