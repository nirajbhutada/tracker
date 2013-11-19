from itertools import chain
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.html import escape, conditional_escape

class GroupedCheckboxSelectMultiple(forms.SelectMultiple):

    def split_seq(self, list, cols=3):
        start = 0
        for i in xrange(cols):
            stop = start + len(list[i::cols])
            yield list[start:stop]
            start = stop

    def _concat(self, items):
        return "\n".join(items)


    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<label class="sublabel" %s>%s %s</label>' % (label_for, rendered_cb, option_label))

        groups = self.split_seq(output)
        output = ["<div class='genres%d'>" % (col + 1) + self._concat(content) + "</div>" for col, content in enumerate(groups)]

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)


class UnValidatedChoiceField(forms.ChoiceField):
    def __init__(self, *largs, **kargs):
        super(UnValidatedChoiceField, self).__init__(*largs, **kargs)

    def clean(self, value):
        if value:
            return value
        else:
            raise forms.ValidationError("This field is Required")

