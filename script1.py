import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class CurvedTrajectoryController(Node):
    def __init__(self):
        super().__init__('curved_trajectory_controller')

        # Subscriber pentru poziția țestoasei
        self.pose_subscriber = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Publisher pentru comenzi de mișcare
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Punctele traiectoriei
        self.trajectory_points = [
            (x, 5 + math.sin(10 * x) + x )
            for x in [i * 0.1 for i in range(5, 90)]  # x în intervalul [0.5, 10.5] cu pași mici
        ]

        # Indexul punctului curent
        self.current_goal_index = 0
        self.current_pose = None

        # Timer pentru bucla de control
        self.create_timer(0.1, self.control_loop)

    def pose_callback(self, msg):
        """Callback pentru a primi poziția actuală a țestoasei."""
        self.current_pose = msg

    def control_loop(self):
        """Bucla principală de control pentru a urmări traiectoria."""
        if self.current_pose is None or self.current_goal_index >= len(self.trajectory_points):
            return

        # Obține coordonatele punctului țintă
        goal_x, goal_y = self.trajectory_points[self.current_goal_index]

        # Calcul distanță până la punctul țintă
        distance = math.sqrt((goal_x - self.current_pose.x) ** 2 + (goal_y - self.current_pose.y) ** 2)

        # Dacă țestoasa este suficient de aproape de punctul țintă, trece la următorul punct
        if distance < 0.2:
            angle_to_goal = math.atan2(goal_y - self.current_pose.y, goal_x - self.current_pose.x)
            angle_diff = angle_to_goal - self.current_pose.theta

            # Normalizează unghiul
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            if abs(angle_diff) < 0.1:  # Dacă unghiul este aproape corect
                self.current_goal_index += 1
                self.get_logger().info(f'Ajuns la punctul ({goal_x}, {goal_y}). Trec la următorul.')
                return

        # Calcul unghi spre punctul țintă
        angle_to_goal = math.atan2(goal_y - self.current_pose.y, goal_x - self.current_pose.x)
        angle_diff = angle_to_goal - self.current_pose.theta

        # Normalizează diferența de unghi
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Creare mesaj Twist pentru controlul mișcării
        twist_msg = Twist()
        twist_msg.linear.x = min(1.0, distance)  # Reduce viteza liniară când este aproape
        twist_msg.angular.z = max(-1.0, min(4.0 * angle_diff, 1.0))  # Controlează viteza unghiulară

        # Publică comanda
        self.cmd_vel_publisher.publish(twist_msg)

    def clear_trajectory(self):
        """Funcție pentru a șterge traiectoriile anterioare din fereastra turtlesim."""
        clear_service_client = self.create_client(Empty, '/clear')
        if clear_service_client.wait_for_service(timeout_sec=5.0):
            request = Empty.Request()
            clear_service_client.call_async(request)
        else:
            self.get_logger().warn("Serviciul '/clear' nu este disponibil.")


def main(args=None):
    rclpy.init(args=args)

    node = CurvedTrajectoryController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
