class Table :
    LEFT    = 1
    RIGHT   = 2
    CENTER    = 3
    ALIGNMENT = [ LEFT, RIGHT, CENTER ]

    NO_WRAPPING = 1
    WRAP_AROUND = 2
    WRAPPING = [ NO_WRAPPING, WRAP_AROUND ]

    #    trrh height of row, 0 means automatically adjust, use negative for an absolute
    #    trgaph is half of the space between a table cell in width, reduce this one
    #    to get a really tiny column

    def __init__( self, *column_widths, **kwargs ) :

        self.Rows = []

        self.SetAlignment      ( kwargs.pop( 'alignment',         self.LEFT ) )
        self.SetLeftOffset     ( kwargs.pop( 'left_offset',       None      ) )
        self.SetGapBetweenCells( kwargs.pop( 'gap_between_cells', None      ) )
        self.SetColumnWidths   ( *column_widths         )

        assert not kwargs, 'invalid keyword args %s' % kwargs

    def SetAlignment( self, value ) :
        assert value is None or value in self.ALIGNMENT
        self.Alignment = value or self.LEFT
        return self

    def SetLeftOffset( self, value ) :
        self.LeftOffset = value
        return self

    def SetGapBetweenCells( self, value ) :
        self.GapBetweenCells = value
        return self

    def SetColumnWidths( self, *column_widths ) :
        self.ColumnWidths = column_widths
        self.ColumnCount  = len( column_widths )
        return self

    def AddRow( self, *cells ) :
        height = None
        if isinstance( cells[ 0 ], (IntType, FloatType, LongType) ):
            height = int( cells[ 0 ] )
            cells  = cells[ 1 : ]

        #  make sure all of the spans add up to the number of columns
        #  otherwise the table will get corrupted
        if self.ColumnCount != sum( [ cell.Span for cell in cells ] ) :
            raise Exception( 'ColumnCount != the total of this row\'s cell.Spans.' )

        self.Rows.append( ( height, cells ) )

    append = AddRow

class Cell( list ) :
    """
    \clvertalt    Text is top-aligned in cell (the default).
    \clvertalc    Text is centered vertically in cell.
    \clvertalb    Text is bottom-aligned in cell.
    \cltxlrtb    Vertical text aligned left (direction bottom up).
    \cltxtbrl     Vertical text aligned right (direction top down).
    """

    ALIGN_TOP    = 1
    ALIGN_CENTER = 2
    ALIGN_BOTTOM = 3

    FLOW_LR_TB          = 1
    FLOW_RL_TB          = 2
    FLOW_LR_BT          = 3
    FLOW_VERTICAL_LR_TB    = 4
    FLOW_VERTICAL_TB_RL    = 5

    def __init__( self, *params, **kwargs ) :
        super( Cell, self ).__init__()

        self.SetFrame  ( None )
        self.SetMargins( None )

        self.SetAlignment( kwargs.get( 'alignment', self.ALIGN_TOP  ) )
        self.SetFlow     ( kwargs.get( 'flow'     , self.FLOW_LR_TB ) )
        self.SetSpan     ( kwargs.get( 'span',      1               ) )

        self.SetStartVerticalMerge( kwargs.get( 'start_vertical_merge', False ) )
        self.SetVerticalMerge     ( kwargs.get( 'vertical_merge',       False ) )

        self._append = super( Cell, self ).append

        for param in params :
            if   isinstance( param, StringType ) : self.append    ( param )
            elif isinstance( param, Paragraph  ) : self.append    ( param )
            elif isinstance( param, FramePS    ) : self.SetFrame  ( param )
            elif isinstance( param, MarginsPS  ) : self.SetMargins( param )

    def SetFrame( self, value ) :
        self.Frame = value
        return self

    def SetMargins( self, value ) :
        self.Margins = value
        return self

    def SetAlignment( self, value ) :
        assert value in [ self.ALIGN_TOP, self.ALIGN_CENTER, self.ALIGN_BOTTOM ] #, self.ALIGN_TEXT_TOP_DOWN, self.ALIGN_TEXT_BOTTOM_UP ]
        self.Alignment = value

    def SetFlow( self, value ) :
        assert value in [ self.FLOW_LR_TB, self.FLOW_RL_TB, self.FLOW_LR_BT, self.FLOW_VERTICAL_LR_TB, self.FLOW_VERTICAL_TB_RL ]
        self.Flow = value

    def SetSpan( self, value ) :
        #  must be a positive integer
        self.Span = int( max( value, 1 ) )
        return self

    def SetStartVerticalMerge( self, value ) :
        self.StartVerticalMerge    = False
        if value :
            self.StartVerticalMerge = True
        return self

    def SetVerticalMerge( self, value ) :
        self.VerticalMerge    = False
        if value :
            self.VerticalMerge = True
        return self

    def append( self, *params ) :
        [ self._append( param ) for param in params ]

