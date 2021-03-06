from traits.api import Instance, Str, List, Bool, Vetoable, VetoableEvent, Any


class ItemsModified ( Vetoable ):
    """ Type of event fired when a DataContext has values added or removed.
    """

    context = Any #Instance('codetools.contexts.i_context.IContext')
    added = List(Str)
    removed = List(Str)
    modified = List(Str)

    def __repr__(self):
        return ('%s(context=%r, added=%r, removed=%r, modified=%r)' %
            (type(self).__name__, self.context, self.added, self.removed,
                self.modified))

# Define an Event trait which accepts an ItemsModified object:
ItemsModifiedEvent = VetoableEvent( ItemsModified )
