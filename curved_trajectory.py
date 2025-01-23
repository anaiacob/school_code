import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class CurvedTrajectoryController(Node):
    def __init__(self):
        super().__init__('curved_trajectory_controller')
        
        # Publisher pentru comenzi de viteză
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Subscriber pentru poziția țestoasei
        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Poziția curentă a țestoasei
        self.current_pose = None
        
        # Numărul de puncte dorit în traiectorie
        num_points = 100

        # Generarea traiectoriei curbilinii (x între 0.5 și 10.5, y între 0.5 și 10.5)
        self.trajectory_points = [
            (0.5 + i * (10 / (num_points - 1)), 
             5 + 4.5 * math.sin(i * (2 * math.pi / (num_points - 1))))
            for i in range(num_points)
        ]

        self.current_goal_index = 0  # Indexul punctului țintă curent
        
        # Timer pentru a publica comenzile la fiecare 0.1 secunde
        self.timer = self.create_timer(0.1, self.control_loop)

    def pose_callback(self, msg):
        """Callback pentru actualizarea poziției curente."""
        self.current_pose = msg

    def control_loop(self):
        """Buclă de control pentru a naviga spre punctele traiectoriei."""
        if self.current_pose is None:
            return  # Așteaptă să primească poziția curentă

        # Oprește dacă toate punctele au fost parcurse
        if self.current_goal_index >= len(self.trajectory_points):
            self.get_logger().info("Traiectoria completată! Termin procesul.")
            rclpy.shutdown()
            return

        # Obține coordonatele țintei curente
        goal_x, goal_y = self.trajectory_points[self.current_goal_index]

        # Verifică dacă punctul curent este în limitele ferestrei
        if not (0.5 <= goal_x <= 10.5 and 0.5 <= goal_y <= 10.5):
            self.get_logger().warn(f"Punctul ({goal_x}, {goal_y}) este în afara limitelor!")
            self.current_goal_index += 1  # Sari la următorul punct
            return

        # Calcul distanță până la punctul țintă
        distance = math.sqrt((goal_x - self.current_pose.x) ** 2 + (goal_y - self.current_pose.y) ** 2)

        # Dacă am ajuns la țintă, trecem la următorul punct
        if distance < 0.1:
            self.get_logger().info(f"Ajuns la punctul ({goal_x}, {goal_y}). Trec la următorul.")
            self.current_goal_index += 1
            return

        # Calcul unghi spre punctul țintă
        angle_to_goal = math.atan2(goal_y - self.current_pose.y, goal_x - self.current_pose.x)
        angle_diff = angle_to_goal - self.current_pose.theta

        # Normalizează diferența de unghi (pentru a fi între -pi și pi)
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Creare mesaj Twist
        twist_msg = Twist()
        twist_msg.linear.x = 1.0  # Viteză liniară constantă
        twist_msg.angular.z = 4.0 * angle_diff  # Viteză unghiulară proporțională cu diferența de unghi
        
        # Publică comanda de viteză
        self.cmd_vel_publisher.publish(twist_msg)

def main(args=None):
    """Funcția principală pentru inițializarea nodului și rularea buclei."""
    rclpy.init(args=args)
    node = CurvedTrajectoryController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
