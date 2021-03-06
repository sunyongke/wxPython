/////////////////////////////////////////////////////////////////////////////
// Name:        gtk/statbox.cpp
// Purpose:
// Author:      Robert Roebling
// Id:          $Id$
// Copyright:   (c) 1998 Robert Roebling
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

// For compilers that support precompilation, includes "wx.h".
#include "wx/wxprec.h"

#if wxUSE_STATBOX

#include "wx/statbox.h"

#include <gtk/gtk.h>

// constants taken from GTK sources
#define LABEL_PAD 1
#define LABEL_SIDE_PAD 2

//-----------------------------------------------------------------------------
// "size_allocate" from m_widget
//-----------------------------------------------------------------------------

extern "C" {
static void size_allocate(GtkWidget* widget, GtkAllocation* alloc, void*)
{
    // clip label as GTK >= 2.12 does
    GtkWidget* label_widget = gtk_frame_get_label_widget(GTK_FRAME(widget));
    int w = alloc->width -
        2 * widget->style->xthickness - 2 * LABEL_PAD - 2 * LABEL_SIDE_PAD;
    if (w < 0) w = 0;
    if (label_widget->allocation.width > w)
    {
        GtkAllocation alloc2 = label_widget->allocation;
        alloc2.width = w;
        gtk_widget_size_allocate(label_widget, &alloc2);
    }
}
}

//-----------------------------------------------------------------------------
// wxStaticBox
//-----------------------------------------------------------------------------

IMPLEMENT_DYNAMIC_CLASS(wxStaticBox, wxControl)

wxStaticBox::wxStaticBox()
{
}

wxStaticBox::wxStaticBox( wxWindow *parent,
                          wxWindowID id,
                          const wxString &label,
                          const wxPoint& pos,
                          const wxSize& size,
                          long style,
                          const wxString& name )
{
    Create( parent, id, label, pos, size, style, name );
}

bool wxStaticBox::Create( wxWindow *parent,
                          wxWindowID id,
                          const wxString& label,
                          const wxPoint& pos,
                          const wxSize& size,
                          long style,
                          const wxString& name )
{
    if (!PreCreation( parent, pos, size ) ||
        !CreateBase( parent, id, pos, size, style, wxDefaultValidator, name ))
    {
        wxFAIL_MSG( wxT("wxStaticBox creation failed") );
        return false;
    }

    m_widget = GTKCreateFrame(label);
    g_object_ref(m_widget);
    // only base SetLabel needs to be called after GTKCreateFrame
    wxControl::SetLabel(label);

    m_parent->DoAddChild( this );

    PostCreation(size);

    // need to set non default alignment?
    gfloat xalign = 0;
    if ( style & wxALIGN_CENTER )
        xalign = 0.5;
    else if ( style & wxALIGN_RIGHT )
        xalign = 1.0;

    gtk_frame_set_label_align(GTK_FRAME(m_widget), xalign, 0.5);

    if (gtk_check_version(2, 12, 0))
    {
        // for clipping label as GTK >= 2.12 does
        g_signal_connect(m_widget, "size_allocate",
            G_CALLBACK(size_allocate), NULL);
    }

    return true;
}

void wxStaticBox::SetLabel( const wxString& label )
{
    wxCHECK_RET( m_widget != NULL, wxT("invalid staticbox") );

    GTKSetLabelForFrame(GTK_FRAME(m_widget), label);
}

void wxStaticBox::DoApplyWidgetStyle(GtkRcStyle *style)
{
    GTKFrameApplyWidgetStyle(GTK_FRAME(m_widget), style);
}

bool wxStaticBox::GTKWidgetNeedsMnemonic() const
{
    return true;
}

void wxStaticBox::GTKWidgetDoSetMnemonic(GtkWidget* w)
{
    GTKFrameSetMnemonicWidget(GTK_FRAME(m_widget), w);
}

// static
wxVisualAttributes
wxStaticBox::GetClassDefaultAttributes(wxWindowVariant WXUNUSED(variant))
{
    return GetDefaultAttributesFromGTKWidget(gtk_frame_new);
}


void wxStaticBox::GetBordersForSizer(int *borderTop, int *borderOther) const
{
    const int BORDER = 5; // FIXME: hardcoded value

    *borderTop = GetLabel().empty() ? 2*BORDER : GetCharHeight();
    *borderOther = BORDER;
}

#endif // wxUSE_STATBOX
