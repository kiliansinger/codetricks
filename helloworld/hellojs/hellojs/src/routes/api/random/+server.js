import { json } from '@sveltejs/kit';

export function GET({url}) {
	let from = Number(url.searchParams.get('from'));
	let to =Number(url.searchParams.get('to'));
	const num = Math.floor(Math.random() * (to-from) + from);
    console.log(num,from,to);
	return new Response(JSON.stringify({number:num}), {
		headers: {
			'Content-Type': 'application/json'
		}
	});
}

