import java.awt.*;

public class Board {
	public final static int X = 0;
	public final static int Y = 1;
	
	public final static int VERTICAL = 0;
	public final static int HORIZONTAL = 1;
	public final static int DIAGONAL_R = 2;
	public final static int DIAGONAL_L = 3;
	
	public final static int[] SIZE = { GameMain.COLS, GameMain.ROWS };
	
	int[][] cells;
	
	public Board() {
		init();
	}
	
	public void init() {
		cells = new int[GameMain.ROWS][GameMain.COLS];
	}
	
	public boolean insert( int col, int player ) {
		int i = GameMain.ROWS-1;
		while( i >= 0 ) {
			if( cells[i][col] == 0 && i > 0 ) {
				i--;
				
			} else if( i < GameMain.ROWS-1 ) {
				if( cells[i][col] > 0 ) i++;
				cells[i][col] = player;
				return true;
				
			} else {
				return false;
			}
		}
		return false;
	}
	
	public int getWinner() {
		int[][] dmap = {{0,1},{1,0},{1,1},{-1,1}};
		String[] dnames = {"VERTICAL", "HORIZONTAL", "DIAGONAL_R", "DIAGONAL_L"};
		
		for( int direction = 0; direction < 4; direction++ ) {
			//System.err.println( dnames[direction] );
			int size = direction < 1 ? GameMain.COLS : GameMain.ROWS;
			for( int i = 0; i < size; i++ ) {
				int[] midPoint = getMidPoint( direction, i );
				int toCheck = cells[midPoint[Y]][midPoint[X]];
				//System.err.println( "MP: [" + midPoint[X] + "," + midPoint[Y] + "], V: " + toCheck );
				
				if( toCheck > 0 ) {
					int[] pos = getStart( midPoint, direction );
					int count = 0;
					
					while( isLegal( pos ) == true ) {
						if( cells[pos[Y]][pos[X]] == toCheck ) count++;
						else count = 0;
						
						//System.err.println( "       (" + pos[X] + "," + pos[Y] + "):  v[" + cells[pos[Y]][pos[X]] + "]   c[" + count + "]");
						
						if( count == 4 ) return toCheck;
						pos[X] += dmap[direction][X];
						pos[Y] += dmap[direction][Y];
					}
				}
			}
		}
		
		return 0;
	}
	
	public boolean isLegal( int[] pos ) {
		for( int i = 0; i < pos.length; i++ ) {
			if( pos[i] < 0 || pos[i] >= SIZE[i] ) return false;
		}
		
		return true;
	}
	
	public int[] getStart( int[] pos, int dir ) {
		int[] start = new int[2];
		int ceil;
		
		if( dir == VERTICAL || dir == HORIZONTAL ) {
			ceil = 1-dir;
			start[1-ceil] = pos[1-ceil];
			
		} else if( dir == DIAGONAL_R ) {
			ceil = SIZE[X] - pos[X] < SIZE[Y] - SIZE[Y] ? X : Y;
			start[ceil] = SIZE[ceil] - ( SIZE[ceil] - pos[ceil] + pos[1-ceil] );
			
		} else if( dir == DIAGONAL_L ) {
			ceil = pos[X] < SIZE[Y] - pos[Y] ? X : Y;
			start[1-ceil] = ceil*( SIZE[X] - 1 );
			if( ceil == 1 ) start[ceil] = pos[ceil] - ( SIZE[1-ceil] - 1 ) - pos[1-ceil];
			else start[ceil] = SIZE[ceil] - pos[ceil] + pos[1-ceil] - 1;
		}
		
		return start;
	}
	
	public int[] getMidPoint( int direction, int increment ) {
		int[] mid = new int[2];
		int i = direction == VERTICAL ? 0 : 1;
		
		mid[i] = increment;
		mid[1-i] = SIZE[1-i]/2;
		return mid;
	}
	
	public void paint(Graphics g) {
		// Draw the grid-lines
		g.setColor( Color.GRAY );
		for( int row = 0; row < GameMain.ROWS; row++ ) {
			g.fillRoundRect( 0, GameMain.CELL_SIZE * row - GameMain.GRID_WIDTH/2, GameMain.CANVAS_WIDTH - 1, GameMain.GRID_WIDTH, GameMain.GRID_WIDTH, GameMain.GRID_WIDTH );
		}
		
		for( int col = 0; col < GameMain.COLS; col++ ) {
			g.fillRoundRect( GameMain.CELL_SIZE * col - GameMain.GRID_WIDTH/2, 0, GameMain.GRID_WIDTH, GameMain.CANVAS_HEIGHT - 1, GameMain.GRID_WIDTH, GameMain.GRID_WIDTH );
		}
		
		// Draw all cells
		Graphics2D g2d = (Graphics2D)g;
		g2d.setStroke( new BasicStroke( GameMain.SYMBOL_STROKE_WIDTH, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
		Color[] colList = { Color.red, Color.blue };
		
		for( int row = 0; row < GameMain.ROWS; row++ ) {
			for( int col = 0; col < GameMain.COLS; col ++ ) {
				int state = cells[row][col];
				if( state != GameMain.EMPTY ) {
					g2d.setColor( colList[state-1] );
					int x = col * GameMain.CELL_SIZE + GameMain.CELL_PADDING;
					int y = ((GameMain.ROWS-1)-row) * GameMain.CELL_SIZE + GameMain.CELL_PADDING;
					g2d.drawOval( x, y, GameMain.SYMBOL_SIZE, GameMain.SYMBOL_SIZE );
				}
			}
		}
	}
}