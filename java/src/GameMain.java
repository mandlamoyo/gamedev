import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

//@SuppressWarnings("serial")
public class GameMain extends JPanel {
	public static final String TITLE = "Connect 4";
	public final static boolean FAILED = false;
	
	public final static int EMPTY = 0;
	public final static int PLAYER1 = 1;
	public final static int PLAYER2 = 2;
	public final static int DRAW = 3;
	
	public static final int ROWS = 6;
	public static final int COLS = 7;
	public static final int CELL_SIZE = 100;
	
	public static final int CANVAS_HEIGHT = CELL_SIZE * ROWS;
	public static final int CANVAS_WIDTH = CELL_SIZE * COLS;
	
	public static final int GRID_WIDTH = 8;  
	public static final int CELL_PADDING = CELL_SIZE/6;
	public static final int SYMBOL_SIZE = CELL_SIZE - CELL_PADDING * 2;
	public static final int SYMBOL_STROKE_WIDTH = 8;
	
	
	
	private Board board;
	private GameState currentState;
	private JLabel statusBar;
	private int currentPlayer;

	public GameMain() {
		
		// MouseEvent manager
		this.addMouseListener( new MouseAdapter() {
			@Override
			public void mouseClicked( MouseEvent e ) {
				boolean res;
				int mouseX = e.getX();
				int mouseY = e.getY();
				
				int rowSelected = mouseY/CELL_SIZE;
				int colSelected = mouseX/CELL_SIZE;
				
				if( currentState == GameState.PLAYING ) {
					if( rowSelected >= 0 && rowSelected < ROWS && colSelected >= 0 && colSelected < COLS && board.cells[rowSelected][colSelected] == EMPTY ) {
						//board.cells[rowSelected][colSelected] = currentPlayer;
						do {
							res = board.insert( colSelected, currentPlayer );
						}
						while( res == FAILED );
						
						updateState( rowSelected, colSelected );
						currentPlayer = 1 + (1 - ( currentPlayer-1 )) ;
					}
				} else {
					initGame();
				}
				
				repaint();
			}
		});
		
		// Setup the status bar (JLabel) to display status message
		statusBar = new JLabel("         ");
		statusBar.setFont( new Font( Font.DIALOG_INPUT, Font.BOLD, 14 ));
		statusBar.setBorder( BorderFactory.createEmptyBorder( 2, 5, 4, 5 ));
		statusBar.setOpaque( true );
		statusBar.setBackground( Color.LIGHT_GRAY );
		
		setLayout( new BorderLayout() );
		add( statusBar, BorderLayout.PAGE_END );
		setPreferredSize( new Dimension( CANVAS_WIDTH, CANVAS_HEIGHT + 30 ));
		
		board = new Board();
		initGame();
	}
	
	public void initGame() {
		board.init();
		currentState = GameState.PLAYING;
		currentPlayer = PLAYER1;
	}
	
	public void updateState( int row, int col ) {
		currentState = GameState.values()[board.getWinner()];
	}
	
	@Override
	public void paintComponent( Graphics g ) {
		super.paintComponent( g );
		setBackground( Color.WHITE );
		board.paint( g );
		
		switch( currentState ) {
			case PLAYING:
				statusBar.setForeground( Color.BLACK );
				if( currentPlayer == PLAYER1 ) statusBar.setText( "Player 1's Turn" );
				else statusBar.setText( "Player 2's Turn" );
				break;
				
			case PLAYER1_WIN:
				statusBar.setForeground( Color.RED );
				statusBar.setText( "Player 1 wins! Click to play again.." );
				break;
				
			case PLAYER2_WIN:
				statusBar.setForeground( Color.RED );
				statusBar.setText( "Player 2 wins! Click to play again.." );
				break;
				
			case DRAW:
				statusBar.setForeground( Color.RED );
				statusBar.setText( "It's a Draw! Click to play again.." );
				break;
				
			default:
				break;
			
		}
	}
	
	public static void main( String[] args ) {
		javax.swing.SwingUtilities.invokeLater( new Runnable() {
			public void run() {
				JFrame frame = new JFrame( TITLE );
				frame.setContentPane( new GameMain() );
				frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE );
				frame.pack();
				frame.setLocationRelativeTo( null );
				frame.setVisible( true );
			}
		});
	}
}