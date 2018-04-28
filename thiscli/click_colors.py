# Initially based on https://github.com/r-m-n/click-help-colors
# with modifications and simplifications.
#
# Originally licensed under the MIT license. See
# https://github.com/r-m-n/click-help-colors/blob/master/LICENSE.txt
import click


class HelpColorsFormatter(click.HelpFormatter):
    def write_usage(self, prog, args='', prefix='Usage: '):
        colorized_prefix = click.style(prefix, fg='white', bold=True)
        super(HelpColorsFormatter, self).write_usage(prog, args,
                                                     prefix=colorized_prefix)

    def write_heading(self, heading):
        colorized_heading = click.style(heading, fg='white', bold=True)
        super(HelpColorsFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows, **kwargs):
        colorized_rows = [(click.style(row[0], fg='green'), row[1])
                          for row in rows]
        super(HelpColorsFormatter, self).write_dl(colorized_rows, **kwargs)


class HelpColorsMixin(object):
    def __init__(self, post_sections=None, *args, **kwargs):
        self.post_sections = post_sections or []
        super().__init__(*args, **kwargs)

    def get_help(self, ctx):
        formatter = HelpColorsFormatter(width=ctx.terminal_width,
                                        max_width=ctx.max_content_width)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip('\n')

    def format_help(self, ctx, formatter):
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_post_sections(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(self, ctx, formatter):
        if self.help:
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(click.style(self.help, fg='blue'))

    def format_post_sections(self, ctx, formatter):
        for title, text in self.post_sections:
            with formatter.section(title):
                formatter.write_text(text)


class HelpColorsGroup(HelpColorsMixin, click.Group):
    def command(self, *args, **kwargs):
        kwargs.setdefault('cls', HelpColorsCommand)
        return super(HelpColorsGroup, self).command(*args, **kwargs)

    def group(self, *args, **kwargs):
        kwargs.setdefault('cls', HelpColorsGroup)
        return super(HelpColorsGroup, self).group(*args, **kwargs)


class HelpColorsCommand(HelpColorsMixin, click.Command):
    pass
