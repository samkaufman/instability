# instability #

A silly little script for moving your Readability queue to Instapaper. It uses Instapaper's Simple API, which is subject to a low rate limit (on the order of, I think, 150 additions per day).

You will need:

 - Readability API key and secret, which you can obtain via your [Account Connections page](https://www.readability.com/account/connections/). Provide it on the command line or with environment variables. (`-k` and `-s` or `READABILITY_KEY` and `READABILITY_SECRET`).

 - An Instapaper account.


## Avoiding the Instapaper Rate Limit ##

instability can avoid adding URLs to Instapaper that are already there. Before running instability, download a CSV of your [current Instapaper queue](http://www.instapaper.com/u) and provide the path on the command line with `-i`.

This can help split the process over multiple days if you re-download said CSV before each invocation of the script.


## How to Use

After grabbing your Instapaper CSV and saving it as instapaper-export.csv... an example:

	export READABILITY_KEY="joejon"
	export READABILITY_SECRET="YQMFG8UyVrHMxc4wxDJfGnNVrHyctELR"
	python -i instapaper-export.csv


## License

ISC license.

	Copyright (c) 2013, Sam Kaufman <emrysk@gmail.com>

	Permission to use, copy, modify, and/or distribute this software for any
	purpose with or without fee is hereby granted, provided that the above
	copyright notice and this permission notice appear in all copies.

	THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
	WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
	MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
	ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
	WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
	ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
	OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.