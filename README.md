## Live Site

Please take a look at the [live site](https://ultrawidesnowboards.com)

## Author

**Cody Lewis**
- <https://github.com/srlm-io>


## Notes

To install, you'll need to

```
sudo apt install ruby ruby-dev ruby-bundler zlib1g-dev
sudo gem install jekyll
cd /path/to/repo
bundle install --path vendor/bundle
```

To run use
```
bundle exec jekyll serve --drafts --watch
````

The site will appear at [http://127.0.0.1:4000](http://127.0.0.1:4000), and you can develop drafts in the `_drafts` folder.

This site is based on the Millennial template [here](https://github.com/LeNPaul/Millennial). Take a look there for markdown examples.

## Setup

Enable git hooks to run:

```bash
git config --local core.hooksPath .githooks/
```

## License

Code is open sourced under the [MIT license](LICENSE.md).

## Development

Set image to a height of 600px, keep proportional.

```bash
mogrify -geometry x600 superpig.jpeg
```


```bash
mogrify -geometry x300 logo.jpg
```

```bash
optipng filename.png
```

```bash
mogrify -quality "40%" -filter Lanczos -interlace Plane -gaussian-blur 0.15 background.jpg
```


## Favicon

Export as png

```bash
convert -background none favicon.svg -define icon:auto-resize favicon.ico
```
