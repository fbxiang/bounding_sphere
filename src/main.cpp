#include <CGAL/Cartesian_d.h>
#include <CGAL/Exact_rational.h>
#include <CGAL/Min_sphere_of_spheres_d.h>
#include <CGAL/Random.h>

const int D = 3;
typedef double FT;
typedef CGAL::Cartesian_d<FT> K;
typedef CGAL::Min_sphere_of_spheres_d_traits_d<K, FT, 3> Traits;
typedef CGAL::Min_sphere_of_spheres_d<Traits> Min_sphere;
typedef K::Point_d Point;
typedef Traits::Sphere Sphere;

struct ResultSphere {
  double x, y, z, r;
};

extern "C" ResultSphere min_sphere(double *points, size_t count) {
  std::vector<Sphere> S;
  for (size_t i = 0; i < count; ++i) {
    S.push_back(Sphere(Point(D, &points[3 * i], &points[3 * i + D]), 0.0));
  }
  Min_sphere ms(S.begin(), S.end());

  std::vector<double> center(ms.center_cartesian_begin(),
                             ms.center_cartesian_end());
  return {center.at(0), center.at(1), center.at(2), ms.radius()};
}

// g++ -O3 -fPIC -shared main.cpp -o _C.so
