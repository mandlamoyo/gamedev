import java.awt.*;

public class Board {
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
	
	public GameState getWinner() {
		// FILL ME PROPERLY
		return GameState.PLAYING;
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