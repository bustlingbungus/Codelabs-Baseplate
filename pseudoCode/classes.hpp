#include <vector>
using namespace std;

struct Vector2 {
    float x, y;
};


class GameObject
{
    public:

        Vector2 pos;
        Vector2 scale;

        vector<GameObject*> components;

        virtual void Update() { }

        virtual void UpdateComponents() {
            for (auto& c : components) {
                c->Update();
                c->UpdateComponents();
            }
        }
};